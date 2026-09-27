package com.civic.complaint.repository;

import com.civic.complaint.entity.SLARule;
import com.civic.complaint.entity.Priority;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface SLARuleRepository extends JpaRepository<SLARule, Long> {
    Optional<SLARule> findByPriority(Priority priority);
}
