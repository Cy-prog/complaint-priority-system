package com.civic.complaint.repository;

import com.civic.complaint.entity.ComplaintFeedback;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ComplaintFeedbackRepository extends JpaRepository<ComplaintFeedback, Long> {
    List<ComplaintFeedback> findByComplaintIdOrderByCreatedAtDesc(Long complaintId);
}
