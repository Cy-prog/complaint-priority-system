package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "escalations")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class Escalation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "complaint_id", nullable = false)
    private Long complaintId;

    @Column(name = "ticket_id", length = 20)
    private String ticketId;

    @Column(name = "from_level", nullable = false)
    private Integer fromLevel;

    @Column(name = "to_level", nullable = false)
    private Integer toLevel;

    @Column(nullable = false, length = 100)
    private String reason;

    @Column(name = "escalated_by", length = 100)
    private String escalatedBy;

    @Column(name = "escalated_by_user_id")
    private Long escalatedByUserId;

    @Column(name = "is_auto", nullable = false)
    @Builder.Default
    private Boolean isAuto = false;

    @CreationTimestamp
    @Column(name = "escalated_at", updatable = false)
    private LocalDateTime escalatedAt;
}
