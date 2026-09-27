package com.civic.complaint.controller.api;

import com.civic.complaint.dto.*;
import com.civic.complaint.entity.*;
import com.civic.complaint.repository.*;
import com.civic.complaint.service.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
@SuppressWarnings("null")
public class ApiController {

    private final ComplaintService complaintService;
    private final AnalyticsService analyticsService;
    private final AIService aiService;
    private final UserRepository userRepo;
    private final CategoryRepository catRepo;
    private final NotificationRepository notificationRepo;

    public ApiController(ComplaintService complaintService, AnalyticsService analyticsService,
                        AIService aiService, UserRepository userRepo,
                        CategoryRepository catRepo, NotificationRepository notificationRepo) {
        this.complaintService = complaintService;
        this.analyticsService = analyticsService;
        this.aiService = aiService;
        this.userRepo = userRepo;
        this.catRepo = catRepo;
        this.notificationRepo = notificationRepo;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> status = new HashMap<>();
        status.put("status", "UP");
        status.put("aiService", aiService.isHealthy() ? "UP" : "DOWN");
        return ResponseEntity.ok(status);
    }

    @GetMapping("/categories")
    public ResponseEntity<List<Category>> getCategories() {
        return ResponseEntity.ok(catRepo.findAll());
    }

    @GetMapping("/dashboard/summary")
    public ResponseEntity<DashboardDTO> dashboardSummary() {
        return ResponseEntity.ok(analyticsService.getDashboardSummary());
    }

    @GetMapping("/dashboard/category-distribution")
    public ResponseEntity<List<Map<String, Object>>> categoryDistribution() {
        return ResponseEntity.ok(analyticsService.getCategoryDistribution());
    }

    @GetMapping("/dashboard/priority-distribution")
    public ResponseEntity<List<Map<String, Object>>> priorityDistribution() {
        return ResponseEntity.ok(analyticsService.getPriorityDistribution());
    }

    @GetMapping("/dashboard/trend")
    public ResponseEntity<List<Map<String, Object>>> trend(@RequestParam(defaultValue = "30") int days) {
        return ResponseEntity.ok(analyticsService.getComplaintsTrend(days));
    }

    @GetMapping("/complaints")
    public ResponseEntity<Page<Complaint>> listComplaints(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String search) {
        PageRequest pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        Page<Complaint> result = search != null && !search.isBlank()
                ? complaintService.search(search, pageable)
                : complaintService.listAll(pageable);
        return ResponseEntity.ok(result);
    }

    @GetMapping("/complaints/{ticketId}")
    public ResponseEntity<Complaint> getComplaint(@PathVariable String ticketId) {
        return ResponseEntity.ok(complaintService.getByTicketId(ticketId));
    }

    @PostMapping("/complaints")
    public ResponseEntity<Map<String, Object>> createComplaint(
            @RequestBody ComplaintCreateDTO dto, Authentication auth) {
        User user = auth != null ? userRepo.findByUsername(auth.getName()).orElse(null) : null;
        Complaint c = complaintService.createComplaint(dto,
                user != null ? user.getId() : null,
                user != null ? user.getFullName() : dto.getCitizenName());
        Map<String, Object> result = new HashMap<>();
        result.put("ticketId", c.getTicketId());
        result.put("message", "Complaint submitted successfully");
        return ResponseEntity.ok(result);
    }

    @PostMapping("/complaints/{ticketId}/override")
    public ResponseEntity<Map<String, Object>> overrideComplaintPriority(
            @PathVariable String ticketId,
            @RequestBody PriorityOverrideDTO dto,
            Authentication auth) {
        String username = (auth != null && auth.getName() != null) ? auth.getName() : "admin";
        User user = userRepo.findByUsername(username).orElse(null);
        Long userId = (user != null) ? user.getId() : 1L;

        PriorityOverride override = complaintService.overridePriority(ticketId, dto, userId, username);

        Map<String, Object> response = new HashMap<>();
        response.put("status", "success");
        response.put("ticketId", ticketId);
        response.put("newPriority", override.getNewPriority().name());
        response.put("newScore", override.getNewScore());
        response.put("reason", override.getReason());
        response.put("message", "Priority overridden successfully");
        return ResponseEntity.ok(response);
    }

    @GetMapping("/notifications")
    public ResponseEntity<Map<String, Object>> getNotifications(Authentication auth) {
        Map<String, Object> result = new HashMap<>();
        if (auth != null && auth.getName() != null) {
            User user = userRepo.findByUsername(auth.getName()).orElse(null);
            if (user != null) {
                result.put("unread", notificationRepo.countByUserIdAndIsReadFalse(user.getId()));
                result.put("notifications",
                    notificationRepo.findByUserIdAndIsReadFalseOrderByCreatedAtDesc(user.getId()));
            }
        }
        return ResponseEntity.ok(result);
    }

    @PostMapping("/notifications/{id}/read")
    public ResponseEntity<Map<String, String>> markRead(@PathVariable Long id) {
        notificationRepo.findById(id).ifPresent(n -> {
            n.setIsRead(true);
            notificationRepo.save(n);
        });
        return ResponseEntity.ok(Map.of("status", "ok"));
    }

    @GetMapping("/ai/status")
    public ResponseEntity<Map<String, Object>> aiStatus() {
        return ResponseEntity.ok(aiService.getModelStatus());
    }

    @GetMapping("/ai/metrics")
    public ResponseEntity<Map<String, Object>> aiMetrics() {
        return ResponseEntity.ok(aiService.getModelMetrics());
    }

    @PostMapping("/ai/quick-scan")
    public ResponseEntity<Map<String, Object>> quickScan(@RequestBody(required = false) Map<String, String> payload) {
        String text = (payload != null && payload.containsKey("text")) ? payload.get("text") : "";
        return ResponseEntity.ok(aiService.quickScan(text));
    }
}
