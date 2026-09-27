package com.civic.complaint.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.*;
import java.util.List;
import java.util.Map;

/**
 * DTO for receiving AI analysis results from the Flask service.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonIgnoreProperties(ignoreUnknown = true)
public class AIAnalysisResponse {
    private String category;
    private String subcategory;
    private Double categoryConfidence;
    private String sentiment;
    private Double sentimentConfidence;
    private Integer severityScore;
    private String priority;
    private Integer priorityScore;
    private Double priorityConfidence;
    private Integer urgencyScore;
    private Integer impactScore;
    private Integer safetyScore;
    private Integer durationScore;
    private Integer disruptionScore;
    private Integer vulnerabilityScore;
    private String summary;
    private List<String> entities;
    private Double entityConfidence;
    private List<String> keyIssues;
    private List<String> reasons;
    private String incidentType;
    private Map<String, Object> vehicle;
    private String approximateTime;
    private String direction;
    private Boolean injuryReported;
    private String affectedPopulation;
    private Integer affectedPopulationEstimate;
    private String reasoningSummary;
    private String recommendedAction;
    private Double confidence;
    private Double duplicateProbability;
    private List<Long> similarComplaintIds;
    private List<Map<String, Object>> similarIncidents;
    private Map<String, String> provenance;
    private String riskLevel;
    private String modelVersion;
    private Double analysisLatencyMs;
}
