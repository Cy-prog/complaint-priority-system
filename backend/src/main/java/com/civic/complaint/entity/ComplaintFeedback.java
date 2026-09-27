package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "complaint_feedback")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class ComplaintFeedback {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "complaint_id", nullable = false)
    private Long complaintId;

    @Column(name = "ticket_id", length = 20)
    private String ticketId;

    @Column(name = "feedback_type", nullable = false, length = 50)
    private String feedbackType;

    @Column(name = "original_value")
    private String originalValue;

    @Column(name = "corrected_value")
    private String correctedValue;

    @Column(columnDefinition = "TEXT")
    private String reason;

    private Integer rating;

    @Column(columnDefinition = "TEXT")
    private String comments;

    @Column(name = "submitted_by_user_id", nullable = false)
    private Long submittedByUserId;

    @Column(name = "submitted_by_username", length = 50)
    private String submittedByUsername;

    @Column(name = "used_for_training", nullable = false)
    @Builder.Default
    private Boolean usedForTraining = false;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
