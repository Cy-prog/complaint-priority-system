package com.civic.complaint.repository;

import com.civic.complaint.entity.AITrainingRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface AITrainingRecordRepository extends JpaRepository<AITrainingRecord, Long> {
    List<AITrainingRecord> findByIsValidatedTrueAndIsUsedForTrainingFalse();
    long countByIsValidatedTrue();
    long countByIsUsedForTrainingTrue();
    long countBySource(String source);
}
