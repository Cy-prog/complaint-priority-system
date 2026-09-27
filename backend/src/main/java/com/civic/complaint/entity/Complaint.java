package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "complaints", indexes = {
    @Index(name = "idx_ticket_id", columnList = "ticket_id"),
    @Index(name = "idx_status", columnList = "status"),
    @Index(name = "idx_created_at", columnList = "created_at")
})
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class Complaint {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "ticket_id", nullable = false, unique = true, length = 20)
    private String ticketId;

    @Column(name = "citizen_id")
    private Long citizenId;

    @Column(name = "citizen_name", length = 100)
    private String citizenName;

    @Column(length = 15)
    private String mobile;

    @Column(length = 200)
    private String topic;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String description;

    @Column(length = 500)
    private String address;

    private Double latitude;
    private Double longitude;

    // AI-assigned fields
    @Column(length = 100)
    private String category;

    @Column(name = "sub_category", length = 100)
    private String subCategory;

    @Column(length = 30)
    private String sentiment;

    @Column(name = "severity_score")
    private Integer severityScore;

    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    private Priority priority;

    @Column(name = "priority_score")
    private Integer priorityScore;

    @Column(name = "ai_confidence")
    private Double aiConfidence;

    @Column(name = "ai_summary", columnDefinition = "TEXT")
    private String aiSummary;

    @Column(name = "extracted_entities", columnDefinition = "TEXT")
    private String extractedEntities;

    // Assignment
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "assigned_department_id")
    private Department assignedDepartment;

    @Column(name = "assigned_officer", length = 100)
    private String assignedOfficer;

    @Column(name = "assigned_officer_id")
    private Long assignedOfficerId;

    // Status
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    @Builder.Default
    private ComplaintStatus status = ComplaintStatus.SUBMITTED;

    @Column(name = "sla_deadline")
    private LocalDateTime slaDeadline;

    @Column(name = "escalation_level")
    @Builder.Default
    private Integer escalationLevel = 0;

    // Timestamps
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "resolved_at")
    private LocalDateTime resolvedAt;

    @Column(name = "resolution_notes", columnDefinition = "TEXT")
    private String resolutionNotes;

    @Column(name = "citizen_feedback", columnDefinition = "TEXT")
    private String citizenFeedback;

    @Column(name = "citizen_feedback_rating")
    private Integer citizenFeedbackRating;

    @Column(name = "ai_model_version", length = 50)
    private String aiModelVersion;

    // Evidence
    @Column(name = "attachment_path", length = 500)
    private String attachmentPath;

    @Column(name = "resolution_photo", length = 500)
    private String resolutionPhoto;

    // Relationships
    @OneToOne(mappedBy = "complaint", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private ComplaintAnalysis analysis;

    @OneToMany(mappedBy = "complaint", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @OrderBy("changedAt DESC")
    @Builder.Default
    private List<ComplaintStatusHistory> statusHistory = new ArrayList<>();

    @OneToMany(mappedBy = "complaint", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @OrderBy("changedAt DESC")
    @Builder.Default
    private List<PriorityOverride> priorityOverrides = new ArrayList<>();

    @OneToOne(mappedBy = "complaint", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private SLARecord slaRecord;
}
