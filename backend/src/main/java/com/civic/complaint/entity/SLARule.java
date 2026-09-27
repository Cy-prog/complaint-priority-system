package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "sla_rules")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class SLARule {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, unique = true, length = 20)
    private Priority priority;

    @Column(name = "response_hours", nullable = false)
    private Integer responseHours;

    @Column(name = "resolution_hours", nullable = false)
    private Integer resolutionHours;

    @Column(name = "is_active", nullable = false)
    @Builder.Default
    private Boolean isActive = true;
}
