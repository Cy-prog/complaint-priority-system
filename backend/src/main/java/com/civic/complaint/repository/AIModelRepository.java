package com.civic.complaint.repository;

import com.civic.complaint.entity.AIModel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface AIModelRepository extends JpaRepository<AIModel, Long> {
    Optional<AIModel> findByModelVersion(String modelVersion);
    Optional<AIModel> findByIsProductionTrue();
    List<AIModel> findAllByOrderByCreatedAtDesc();
}
