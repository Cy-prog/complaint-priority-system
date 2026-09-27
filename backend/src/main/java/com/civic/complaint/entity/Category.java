package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "categories")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class Category {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String name;

    @Column(length = 500)
    private String description;

    @Column(name = "risk_level", length = 20)
    @Builder.Default
    private String riskLevel = "low";

    @Column(name = "is_essential_service", nullable = false)
    @Builder.Default
    private Boolean isEssentialService = false;

    @Column(name = "default_department", length = 100)
    private String defaultDepartment;

    @Column(name = "is_active", nullable = false)
    @Builder.Default
    private Boolean isActive = true;
}
