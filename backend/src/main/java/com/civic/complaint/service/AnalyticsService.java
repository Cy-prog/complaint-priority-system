package com.civic.complaint.service;

import com.civic.complaint.dto.DashboardDTO;
import com.civic.complaint.entity.ComplaintStatus;
import com.civic.complaint.entity.Priority;
import com.civic.complaint.repository.*;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

@Service
public class AnalyticsService {

    private final ComplaintRepository complaintRepo;
    private final ComplaintAnalysisRepository analysisRepo;
    private final SLARecordRepository slaRepo;
    private final PriorityOverrideRepository overrideRepo;

    public AnalyticsService(ComplaintRepository complaintRepo,
                           ComplaintAnalysisRepository analysisRepo,
                           SLARecordRepository slaRepo,
                           PriorityOverrideRepository overrideRepo) {
        this.complaintRepo = complaintRepo;
        this.analysisRepo = analysisRepo;
        this.slaRepo = slaRepo;
        this.overrideRepo = overrideRepo;
    }

    public DashboardDTO getDashboardSummary() {
        long total = complaintRepo.count();
        long open = complaintRepo.countOpenComplaints();
        long critical = complaintRepo.countByPriority(Priority.CRITICAL);
        long high = complaintRepo.countByPriority(Priority.HIGH);
        long medium = complaintRepo.countByPriority(Priority.MEDIUM);
        long low = complaintRepo.countByPriority(Priority.LOW);
        long resolved = complaintRepo.countResolvedSince(LocalDate.now().atStartOfDay());
        long slaBreached = slaRepo.countByIsBreachedTrue();
        long pending = complaintRepo.countByStatus(ComplaintStatus.SUBMITTED)
                     + complaintRepo.countByStatus(ComplaintStatus.AI_ANALYSIS_PENDING);
        long inProgress = complaintRepo.countByStatus(ComplaintStatus.IN_PROGRESS)
                        + complaintRepo.countByStatus(ComplaintStatus.ASSIGNED);

        Double avgConf = analysisRepo.getAverageConfidence();
        long totalOverrides = overrideRepo.count();
        long lowConf = analysisRepo.countByConfidenceLessThan(0.6);

        double slaCompliance = 0;
        long totalSla = slaRepo.count();
        if (totalSla > 0) {
            slaCompliance = (double)(totalSla - slaBreached) / totalSla * 100;
        }

        long avgConfDisplay = 0;
        if (avgConf != null) {
            avgConfDisplay = avgConf > 1.0 ? Math.round(avgConf) : Math.round(avgConf * 100.0);
        }

        return DashboardDTO.builder()
                .totalComplaints(total)
                .openComplaints(open)
                .criticalCount(critical)
                .highCount(high)
                .mediumCount(medium)
                .lowCount(low)
                .resolvedToday(resolved)
                .slaBreached(slaBreached)
                .pendingCount(pending)
                .inProgressCount(inProgress)
                .avgConfidence(avgConfDisplay)
                .slaComplianceRate(Math.round(slaCompliance * 10.0) / 10.0)
                .totalOverrides(totalOverrides)
                .lowConfidenceCount(lowConf)
                .build();
    }

    public List<Map<String, Object>> getCategoryDistribution() {
        List<Object[]> rows = complaintRepo.countByCategory();
        List<Map<String, Object>> result = new ArrayList<>();
        for (Object[] row : rows) {
            Map<String, Object> item = new HashMap<>();
            item.put("category", row[0]);
            item.put("count", row[1]);
            result.add(item);
        }
        return result;
    }

    public List<Map<String, Object>> getPriorityDistribution() {
        List<Object[]> rows = complaintRepo.countByPriorityGrouped();
        List<Map<String, Object>> result = new ArrayList<>();
        for (Object[] row : rows) {
            Map<String, Object> item = new HashMap<>();
            item.put("priority", row[0] != null ? row[0].toString() : "UNASSIGNED");
            item.put("count", row[1]);
            result.add(item);
        }
        return result;
    }

    public List<Map<String, Object>> getStatusDistribution() {
        List<Object[]> rows = complaintRepo.countByStatusGrouped();
        List<Map<String, Object>> result = new ArrayList<>();
        for (Object[] row : rows) {
            Map<String, Object> item = new HashMap<>();
            item.put("status", row[0] != null ? row[0].toString() : "UNKNOWN");
            item.put("count", row[1]);
            result.add(item);
        }
        return result;
    }

    public List<Map<String, Object>> getComplaintsTrend(int days) {
        LocalDateTime since = LocalDateTime.now().minusDays(days);
        List<Object[]> rows = complaintRepo.countByDateSince(since);
        List<Map<String, Object>> result = new ArrayList<>();
        for (Object[] row : rows) {
            Map<String, Object> item = new HashMap<>();
            item.put("date", row[0] != null ? row[0].toString() : "");
            item.put("count", row[1]);
            result.add(item);
        }
        return result;
    }
}
