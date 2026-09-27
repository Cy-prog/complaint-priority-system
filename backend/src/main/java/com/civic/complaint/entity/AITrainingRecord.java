package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "ai_training_records")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class AITrainingRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "complaint_id")
    private Long complaintId;

    @Column(name = "ticket_id", length = 20)
    private String ticketId;

    @Column(name = "complaint_text", nullable = false, columnDefinition = "TEXT")
    private String complaintText;

    @Column(name = "ai_category", length = 100)
    private String aiCategory;

    @Column(name = "ai_priority", length = 20)
    private String aiPriority;

    @Column(name = "corrected_category", length = 100)
    private String correctedCategory;

    @Column(name = "corrected_priority", length = 20)
    private String correctedPriority;

    @Column(name = "final_resolution", length = 100)
    private String finalResolution;

    @Column(length = 100)
    private String department;

    @Column(name = "model_version", length = 50)
    private String modelVersion;

    @Column(length = 20)
    @Builder.Default
    private String source = "REAL";

    @Column(name = "is_validated", nullable = false)
    @Builder.Default
    private Boolean isValidated = false;

    @Column(name = "validated_by", length = 50)
    private String validatedBy;

    @Column(name = "is_used_for_training", nullable = false)
    @Builder.Default
    private Boolean isUsedForTraining = false;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
