package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "ai_models")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class AIModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "model_version", nullable = false, unique = true, length = 50)
    private String modelVersion;

    @Column(name = "model_type", length = 50)
    @Builder.Default
    private String modelType = "category_classifier";

    @Column(name = "trained_at")
    private LocalDateTime trainedAt;

    @Column(name = "training_dataset_size")
    private Integer trainingDatasetSize;

    private Double accuracy;
    private Double precision_;
    private Double recall;

    @Column(name = "f1_score")
    private Double f1Score;

    @Column(name = "deployment_status", length = 20)
    @Builder.Default
    private String deploymentStatus = "candidate";

    @Column(name = "is_production", nullable = false)
    @Builder.Default
    private Boolean isProduction = false;

    @Column(name = "training_notes", columnDefinition = "TEXT")
    private String trainingNotes;

    @Column(name = "confusion_matrix", columnDefinition = "TEXT")
    private String confusionMatrix;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
