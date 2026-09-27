package com.civic.complaint.repository;

import com.civic.complaint.entity.PriorityOverride;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface PriorityOverrideRepository extends JpaRepository<PriorityOverride, Long> {
    List<PriorityOverride> findByComplaintIdOrderByChangedAtDesc(Long complaintId);
    long countByComplaintId(Long complaintId);
}
