package com.civic.complaint.repository;

import com.civic.complaint.entity.SLARecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface SLARecordRepository extends JpaRepository<SLARecord, Long> {
    Optional<SLARecord> findByComplaintId(Long complaintId);
    List<SLARecord> findByIsBreachedFalseAndResolvedAtIsNullAndSlaDeadlineBefore(LocalDateTime now);
    long countByIsBreachedTrue();
}
