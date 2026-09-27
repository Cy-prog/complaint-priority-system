package com.civic.complaint.service;

import com.civic.complaint.dto.AIAnalysisResponse;
import com.civic.complaint.dto.ComplaintCreateDTO;
import com.civic.complaint.dto.PriorityOverrideDTO;
import com.civic.complaint.entity.*;
import com.civic.complaint.exception.BadRequestException;
import com.civic.complaint.exception.ResourceNotFoundException;
import com.civic.complaint.repository.*;
import com.civic.complaint.util.TicketIdGenerator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@SuppressWarnings("null")
public class ComplaintService {

    private static final Logger log = LoggerFactory.getLogger(ComplaintService.class);

    private final ComplaintRepository complaintRepo;
    private final ComplaintAnalysisRepository analysisRepo;
    private final StatusHistoryRepository historyRepo;
    private final PriorityOverrideRepository overrideRepo;
    private final SLARecordRepository slaRepo;
    private final SLARuleRepository slaRuleRepo;
    private final AuditLogRepository auditRepo;
    private final NotificationRepository notificationRepo;
    private final AITrainingRecordRepository aiTrainingRepo;
    private final AIService aiService;
    private final TicketIdGenerator ticketIdGenerator;

    public ComplaintService(
            ComplaintRepository complaintRepo,
            ComplaintAnalysisRepository analysisRepo,
            StatusHistoryRepository historyRepo,
            PriorityOverrideRepository overrideRepo,
            SLARecordRepository slaRepo,
            SLARuleRepository slaRuleRepo,
            AuditLogRepository auditRepo,
            NotificationRepository notificationRepo,
            AITrainingRecordRepository aiTrainingRepo,
            AIService aiService,
            TicketIdGenerator ticketIdGenerator) {
        this.complaintRepo = complaintRepo;
        this.analysisRepo = analysisRepo;
        this.historyRepo = historyRepo;
        this.overrideRepo = overrideRepo;
        this.slaRepo = slaRepo;
        this.slaRuleRepo = slaRuleRepo;
        this.auditRepo = auditRepo;
        this.notificationRepo = notificationRepo;
        this.aiTrainingRepo = aiTrainingRepo;
        this.aiService = aiService;
        this.ticketIdGenerator = ticketIdGenerator;
    }

    /**
     * Create a new complaint and trigger async AI analysis.
     */
    @Transactional
    public Complaint createComplaint(ComplaintCreateDTO dto, Long citizenId, String citizenName) {
        // Generate unique ticket ID
        String ticketId;
        int attempts = 0;
        do {
            ticketId = ticketIdGenerator.generate();
            attempts++;
        } while (complaintRepo.findByTicketId(ticketId).isPresent() && attempts < 10);

        if (attempts >= 10) {
            ticketId = ticketIdGenerator.generateWithSuffix();
        }

        Complaint complaint = Complaint.builder()
                .ticketId(ticketId)
                .citizenId(citizenId)
                .citizenName(dto.getCitizenName() != null ? dto.getCitizenName() : citizenName)
                .mobile(dto.getMobile())
                .topic(dto.getTopic())
                .description(dto.getDescription())
                .address(dto.getAddress())
                .latitude(dto.getLatitude())
                .longitude(dto.getLongitude())
                .status(ComplaintStatus.SUBMITTED)
                .build();

        complaint = complaintRepo.save(complaint);

        // Record initial status history
        historyRepo.save(ComplaintStatusHistory.builder()
                .complaint(complaint)
                .oldStatus(ComplaintStatus.SUBMITTED)
                .newStatus(ComplaintStatus.SUBMITTED)
                .changedBy(citizenName != null ? citizenName : "Citizen")
                .changedByUserId(citizenId)
                .note("Complaint submitted")
                .build());

        // Audit log
        auditRepo.save(AuditLog.builder()
                .userId(citizenId)
                .username(citizenName)
                .action("COMPLAINT_CREATED")
                .entityType("complaint")
                .entityId(complaint.getId())
                .newValue(ticketId)
                .build());

        // Trigger AI analysis
        triggerAIAnalysis(complaint.getId());

        return complaint;
    }

    /**
     * Asynchronously analyze a complaint using the AI service.
     */
    @Async("aiTaskExecutor")
    public void triggerAIAnalysis(Long complaintId) {
        try {
            Complaint complaint = complaintRepo.findById(complaintId)
                    .orElseThrow(() -> new ResourceNotFoundException("Complaint not found"));

            complaint.setStatus(ComplaintStatus.AI_ANALYSIS_PENDING);
            complaintRepo.save(complaint);

            AIAnalysisResponse aiResult = aiService.analyzeComplaint(
                    complaint.getTopic(), complaint.getDescription(), complaint.getAddress());

            if (aiResult != null) {
                applyAnalysis(complaint, aiResult);
            }
        } catch (Exception e) {
            log.error("AI analysis failed for complaint {}: {}", complaintId, e.getMessage());
            // Complaint stays in AI_ANALYSIS_PENDING for manual retry
        }
    }

    /**
     * Apply AI analysis result to a complaint.
     */
    @Transactional
    public void applyAnalysis(Complaint complaint, AIAnalysisResponse aiResult) {
        // Map priority string to enum
        Priority priority;
        try {
            priority = Priority.valueOf(aiResult.getPriority().toUpperCase());
        } catch (Exception e) {
            priority = Priority.LOW;
        }

        // Save or update analysis record
        ComplaintAnalysis analysis = analysisRepo.findByComplaintId(complaint.getId())
                .orElseGet(() -> ComplaintAnalysis.builder().complaint(complaint).build());
        double rawConf = (aiResult.getConfidence() != null) ? aiResult.getConfidence() : 0.85;
        double normalizedConf = rawConf > 1.0 ? rawConf / 100.0 : rawConf;

        analysis.setPriority(priority);
        analysis.setPriorityScore(aiResult.getPriorityScore() != null ? aiResult.getPriorityScore() : 0);
        analysis.setUrgencyScore(aiResult.getUrgencyScore() != null ? aiResult.getUrgencyScore() : 0);
        analysis.setSeverityScore(aiResult.getSeverityScore() != null ? aiResult.getSeverityScore() : 0);
        analysis.setImpactScore(aiResult.getImpactScore() != null ? aiResult.getImpactScore() : 0);
        analysis.setSafetyScore(aiResult.getSafetyScore() != null ? aiResult.getSafetyScore() : 0);
        analysis.setDurationScore(aiResult.getDurationScore() != null ? aiResult.getDurationScore() : 0);
        analysis.setConfidence(normalizedConf);
        analysis.setSentiment(aiResult.getSentiment());
        analysis.setRiskLevel(aiResult.getRiskLevel());
        analysis.setEntities(aiResult.getEntities() != null ? String.join(", ", aiResult.getEntities()) : "");
        analysis.setKeyIssues(aiResult.getKeyIssues() != null ? String.join("; ", aiResult.getKeyIssues()) : "");
        analysis.setAffectedPopulation(aiResult.getAffectedPopulation());
        analysis.setAffectedPopulationEstimate(aiResult.getAffectedPopulationEstimate());
        analysis.setReasoningSummary(aiResult.getReasoningSummary());
        analysis.setRecommendedAction(aiResult.getRecommendedAction());
        analysis.setDuplicateProbability(aiResult.getDuplicateProbability() != null ? aiResult.getDuplicateProbability() : 0.0);
        analysis.setAnalysisModelVersion(aiResult.getModelVersion());
        analysis.setAnalysisLatencyMs(aiResult.getAnalysisLatencyMs());
        analysis.setSubcategory(aiResult.getSubcategory());
        analysis.setAiSummary(aiResult.getSummary());

        analysisRepo.save(analysis);

        // Update complaint with AI results
        complaint.setCategory(aiResult.getCategory());
        complaint.setSubCategory(aiResult.getSubcategory());
        complaint.setSentiment(aiResult.getSentiment());
        complaint.setSeverityScore(aiResult.getSeverityScore());
        complaint.setPriority(priority);
        complaint.setPriorityScore(aiResult.getPriorityScore());
        complaint.setAiConfidence(normalizedConf);
        complaint.setAiSummary(aiResult.getSummary());
        complaint.setAiModelVersion(aiResult.getModelVersion());
        complaint.setStatus(ComplaintStatus.CLASSIFIED);

        // Create SLA record
        createSLARecord(complaint, priority);

        complaintRepo.save(complaint);

        // Status history
        historyRepo.save(ComplaintStatusHistory.builder()
                .complaint(complaint)
                .oldStatus(ComplaintStatus.AI_ANALYSIS_PENDING)
                .newStatus(ComplaintStatus.CLASSIFIED)
                .changedBy("AI System")
                .note("AI analysis completed: " + priority + " priority, " +
                      String.format("%.0f%%", normalizedConf * 100) + " confidence")
                .build());

        // Audit
        auditRepo.save(AuditLog.builder()
                .action("AI_ANALYZED")
                .entityType("complaint")
                .entityId(complaint.getId())
                .newValue("Priority=" + priority + ", Category=" + aiResult.getCategory() +
                         ", Confidence=" + String.format("%.2f", normalizedConf))
                .build());

        // Notification for citizen
        if (complaint.getCitizenId() != null) {
            notificationRepo.save(Notification.builder()
                    .userId(complaint.getCitizenId())
                    .type("COMPLAINT_ANALYZED")
                    .title("Complaint Analyzed")
                    .message("Your complaint " + complaint.getTicketId() + " has been analyzed. Priority: " + priority)
                    .complaintId(complaint.getId())
                    .ticketId(complaint.getTicketId())
                    .build());
        }
    }

    /**
     * Create SLA record based on priority.
     */
    private void createSLARecord(Complaint complaint, Priority priority) {
        int resolutionHours = switch (priority) {
            case CRITICAL -> 4;
            case HIGH -> 12;
            case MEDIUM -> 48;
            case LOW -> 168;
        };

        // Check configurable SLA rules
        SLARule rule = slaRuleRepo.findByPriority(priority).orElse(null);
        if (rule != null && rule.getResolutionHours() != null) {
            resolutionHours = rule.getResolutionHours();
        }

        LocalDateTime deadline = LocalDateTime.now().plusHours(resolutionHours);
        complaint.setSlaDeadline(deadline);

        SLARecord slaRecord = slaRepo.findByComplaintId(complaint.getId())
                .orElseGet(() -> SLARecord.builder().complaint(complaint).build());
        slaRecord.setPriority(priority);
        slaRecord.setSlaDeadline(deadline);
        slaRecord.setIsBreached(false);
        slaRepo.save(slaRecord);
    }

    // ─── Retrieval ─────────────────────────────────────────

    public Complaint getByTicketId(String ticketId) {
        return complaintRepo.findByTicketId(ticketId)
                .orElseThrow(() -> new ResourceNotFoundException("Complaint not found: " + ticketId));
    }

    public Complaint getById(Long id) {
        return complaintRepo.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Complaint not found: " + id));
    }

    public Page<Complaint> listAll(Pageable pageable) {
        return complaintRepo.findAll(pageable);
    }

    public Page<Complaint> search(String query, Pageable pageable) {
        return complaintRepo.searchComplaints(query, pageable);
    }

    public List<Complaint> getByCitizenId(Long citizenId) {
        return complaintRepo.findByCitizenIdOrderByCreatedAtDesc(citizenId);
    }

    public List<Complaint> getBycitizenId(Long citizenId) {
        return getByCitizenId(citizenId);
    }

    public Page<Complaint> getByStatus(ComplaintStatus status, Pageable pageable) {
        return complaintRepo.findByStatus(status, pageable);
    }

    public Page<Complaint> getByPriority(Priority priority, Pageable pageable) {
        return complaintRepo.findByPriority(priority, pageable);
    }

    public List<Complaint> getRecent() {
        return complaintRepo.findTop10ByOrderByCreatedAtDesc();
    }

    // ─── Status Updates ────────────────────────────────────

    @Transactional
    public Complaint updateStatus(String ticketId, ComplaintStatus newStatus, Long userId, String username, String note) {
        Complaint complaint = getByTicketId(ticketId);
        ComplaintStatus oldStatus = complaint.getStatus();

        complaint.setStatus(newStatus);
        if (newStatus == ComplaintStatus.RESOLVED || newStatus == ComplaintStatus.CLOSED) {
            complaint.setResolvedAt(LocalDateTime.now());
            // Update SLA record
            slaRepo.findByComplaintId(complaint.getId()).ifPresent(sla -> {
                sla.setResolvedAt(LocalDateTime.now());
                if (complaint.getCreatedAt() != null) {
                    long minutes = java.time.Duration.between(complaint.getCreatedAt(), LocalDateTime.now()).toMinutes();
                    sla.setResolutionTimeMinutes((int) minutes);
                }
                slaRepo.save(sla);
            });
        }

        complaintRepo.save(complaint);

        // Status history
        historyRepo.save(ComplaintStatusHistory.builder()
                .complaint(complaint)
                .oldStatus(oldStatus)
                .newStatus(newStatus)
                .changedBy(username)
                .changedByUserId(userId)
                .note(note != null ? note : "Status changed to " + newStatus)
                .build());

        // Audit
        auditRepo.save(AuditLog.builder()
                .userId(userId)
                .username(username)
                .action("STATUS_CHANGED")
                .entityType("complaint")
                .entityId(complaint.getId())
                .oldValue(oldStatus.name())
                .newValue(newStatus.name())
                .build());

        // Citizen notification
        if (complaint.getCitizenId() != null) {
            notificationRepo.save(Notification.builder()
                    .userId(complaint.getCitizenId())
                    .type("STATUS_CHANGED")
                    .title("Complaint Status Updated")
                    .message("Your complaint " + ticketId + " status changed to: " + newStatus)
                    .complaintId(complaint.getId())
                    .ticketId(ticketId)
                    .build());
        }

        return complaint;
    }

    // ─── Assignment ────────────────────────────────────────

    @Transactional
    public Complaint assignComplaint(String ticketId, Department department, String officer, Long officerId,
                                      Long userId, String username) {
        Complaint complaint = getByTicketId(ticketId);

        complaint.setAssignedDepartment(department);
        complaint.setAssignedOfficer(officer);
        complaint.setAssignedOfficerId(officerId);
        if (complaint.getStatus() == ComplaintStatus.CLASSIFIED) {
            complaint.setStatus(ComplaintStatus.ASSIGNED);
        }

        complaintRepo.save(complaint);

        historyRepo.save(ComplaintStatusHistory.builder()
                .complaint(complaint)
                .oldStatus(complaint.getStatus())
                .newStatus(ComplaintStatus.ASSIGNED)
                .changedBy(username)
                .changedByUserId(userId)
                .note("Assigned to " + department.getName() + (officer != null ? " / " + officer : ""))
                .build());

        auditRepo.save(AuditLog.builder()
                .userId(userId)
                .username(username)
                .action("COMPLAINT_ASSIGNED")
                .entityType("complaint")
                .entityId(complaint.getId())
                .newValue("Department=" + department.getName())
                .build());

        return complaint;
    }

    // ─── Priority Override ─────────────────────────────────

    @Transactional
    public PriorityOverride overridePriority(String ticketId, PriorityOverrideDTO dto, Long userId, String username) {
        if (dto == null || dto.getNewPriority() == null || dto.getNewPriority().isBlank()) {
            throw new BadRequestException("New priority must not be empty");
        }

        Complaint complaint = getByTicketId(ticketId);

        Priority newPriority;
        try {
            newPriority = Priority.valueOf(dto.getNewPriority().trim().toUpperCase());
        } catch (IllegalArgumentException e) {
            throw new BadRequestException("Invalid priority value: " + dto.getNewPriority());
        }

        Priority oldPriority = complaint.getPriority() != null ? complaint.getPriority() : Priority.LOW;
        int oldScore = complaint.getPriorityScore() != null ? complaint.getPriorityScore() : 0;
        Long effectiveUserId = (userId != null) ? userId : 1L;
        String effectiveUsername = (username != null && !username.isBlank()) ? username : "admin";

        final int finalScore = (dto.getNewScore() != null) ? dto.getNewScore() : switch (newPriority) {
            case CRITICAL -> 90;
            case HIGH -> 70;
            case MEDIUM -> 45;
            case LOW -> 15;
        };

        PriorityOverride override = PriorityOverride.builder()
                .complaint(complaint)
                .originalPriority(oldPriority)
                .originalScore(oldScore)
                .newPriority(newPriority)
                .newScore(finalScore)
                .changedByUserId(effectiveUserId)
                .changedByUsername(effectiveUsername)
                .reason(dto.getReason() != null ? dto.getReason().trim() : "Administrative override")
                .build();
        overrideRepo.save(override);

        // Update complaint
        complaint.setPriority(newPriority);
        complaint.setPriorityScore(finalScore);
        complaintRepo.save(complaint);

        // Update analysis if exists
        analysisRepo.findByComplaintId(complaint.getId()).ifPresent(analysis -> {
            analysis.setPriority(newPriority);
            analysis.setPriorityScore(finalScore);
            analysisRepo.save(analysis);
        });

        // Update SLA based on new priority
        createSLARecord(complaint, newPriority);

        // Continuous learning pipeline (Phase 18): Save validated correction record
        try {
            String fullText = (complaint.getTopic() != null ? complaint.getTopic() + ". " : "") + complaint.getDescription();
            aiTrainingRepo.save(AITrainingRecord.builder()
                    .complaintId(complaint.getId())
                    .ticketId(complaint.getTicketId())
                    .complaintText(fullText)
                    .aiCategory(complaint.getCategory())
                    .aiPriority(oldPriority.name())
                    .correctedCategory(complaint.getCategory())
                    .correctedPriority(newPriority.name())
                    .finalResolution(dto.getReason())
                    .department(complaint.getAssignedDepartment() != null ? complaint.getAssignedDepartment().getName() : null)
                    .modelVersion(complaint.getAiModelVersion() != null ? complaint.getAiModelVersion() : "1.1.0")
                    .source("HUMAN_OVERRIDE")
                    .isValidated(true)
                    .validatedBy(effectiveUsername)
                    .isUsedForTraining(false)
                    .build());
        } catch (Exception ex) {
            log.warn("Could not save continuous learning AI training record for {}: {}", ticketId, ex.getMessage());
        }

        // Audit
        auditRepo.save(AuditLog.builder()
                .userId(effectiveUserId)
                .username(effectiveUsername)
                .action("PRIORITY_CHANGED")
                .entityType("complaint")
                .entityId(complaint.getId())
                .oldValue(oldPriority + " (score: " + oldScore + ")")
                .newValue(newPriority + " (score: " + finalScore + ")")
                .details("Reason: " + dto.getReason())
                .build());

        return override;
    }

    // ─── Citizen Feedback ──────────────────────────────────

    @Transactional
    public Complaint submitCitizenFeedback(String ticketId, int rating, String feedback) {
        Complaint complaint = getByTicketId(ticketId);
        complaint.setCitizenFeedback(feedback);
        complaint.setCitizenFeedbackRating(rating);

        if (rating >= 3) {
            complaint.setStatus(ComplaintStatus.CLOSED);
            complaint.setResolvedAt(complaint.getResolvedAt() != null ? complaint.getResolvedAt() : LocalDateTime.now());
        } else {
            complaint.setStatus(ComplaintStatus.REOPENED);
        }

        complaintRepo.save(complaint);

        historyRepo.save(ComplaintStatusHistory.builder()
                .complaint(complaint)
                .oldStatus(ComplaintStatus.RESOLVED)
                .newStatus(complaint.getStatus())
                .changedBy("Citizen")
                .changedByUserId(complaint.getCitizenId())
                .note("Citizen feedback: " + rating + "/5 - " + (feedback != null ? feedback : ""))
                .build());

        return complaint;
    }
}
