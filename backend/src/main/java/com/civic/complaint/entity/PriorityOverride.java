package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "priority_overrides")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class PriorityOverride {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "complaint_id", nullable = false)
    private Complaint complaint;

    @Enumerated(EnumType.STRING)
    @Column(name = "original_priority", nullable = false, length = 20)
    private Priority originalPriority;

    @Column(name = "original_score", nullable = false)
    private Integer originalScore;

    @Enumerated(EnumType.STRING)
    @Column(name = "new_priority", nullable = false, length = 20)
    private Priority newPriority;

    @Column(name = "new_score")
    private Integer newScore;

    @Column(name = "changed_by_user_id")
    private Long changedByUserId;

    @Column(name = "changed_by_username", length = 50)
    private String changedByUsername;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String reason;

    @CreationTimestamp
    @Column(name = "changed_at", updatable = false)
    private LocalDateTime changedAt;
}
