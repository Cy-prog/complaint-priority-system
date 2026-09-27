package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "complaint_analysis")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class ComplaintAnalysis {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "complaint_id", nullable = false, unique = true)
    private Complaint complaint;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private Priority priority;

    @Column(name = "priority_score", nullable = false)
    private Integer priorityScore;

    @Column(name = "urgency_score")
    @Builder.Default
    private Integer urgencyScore = 0;

    @Column(name = "severity_score")
    @Builder.Default
    private Integer severityScore = 0;

    @Column(name = "impact_score")
    @Builder.Default
    private Integer impactScore = 0;

    @Column(name = "safety_score")
    @Builder.Default
    private Integer safetyScore = 0;

    @Column(name = "duration_score")
    @Builder.Default
    private Integer durationScore = 0;

    @Column(nullable = false)
    @Builder.Default
    private Double confidence = 0.0;

    @Column(length = 30)
    private String sentiment;

    @Column(name = "risk_level", length = 20)
    private String riskLevel;

    @Column(columnDefinition = "TEXT")
    private String entities;

    @Column(name = "key_issues", columnDefinition = "TEXT")
    private String keyIssues;

    @Column(name = "affected_population", length = 200)
    private String affectedPopulation;

    @Column(name = "affected_population_estimate")
    private Integer affectedPopulationEstimate;

    @Column(name = "reasoning_summary", columnDefinition = "TEXT")
    private String reasoningSummary;

    @Column(name = "recommended_action", columnDefinition = "TEXT")
    private String recommendedAction;

    @Column(name = "duplicate_probability")
    @Builder.Default
    private Double duplicateProbability = 0.0;

    @Column(name = "analysis_model_version", length = 50)
    private String analysisModelVersion;

    @Column(name = "analysis_latency_ms")
    private Double analysisLatencyMs;

    @Column(length = 100)
    private String subcategory;

    @Column(name = "ai_summary", columnDefinition = "TEXT")
    private String aiSummary;

    @CreationTimestamp
    @Column(name = "analyzed_at", updatable = false)
    private LocalDateTime analyzedAt;
}
