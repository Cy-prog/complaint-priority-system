package com.civic.complaint.dto;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DashboardDTO {
    private long totalComplaints;
    private long openComplaints;
    private long criticalCount;
    private long highCount;
    private long mediumCount;
    private long lowCount;
    private long resolvedToday;
    private long slaBreached;
    private long pendingCount;
    private long inProgressCount;
    private double avgConfidence;
    private double slaComplianceRate;
    private long totalOverrides;
    private long lowConfidenceCount;
}
