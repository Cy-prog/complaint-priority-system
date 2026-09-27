package com.civic.complaint.repository;

import com.civic.complaint.entity.ComplaintAnalysis;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface ComplaintAnalysisRepository extends JpaRepository<ComplaintAnalysis, Long> {
    Optional<ComplaintAnalysis> findByComplaintId(Long complaintId);
    void deleteByComplaintId(Long complaintId);

    @Query("SELECT AVG(a.confidence) FROM ComplaintAnalysis a")
    Double getAverageConfidence();

    long countByConfidenceLessThan(Double threshold);
}
