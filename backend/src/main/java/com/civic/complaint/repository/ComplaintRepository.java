package com.civic.complaint.repository;

import com.civic.complaint.entity.Complaint;
import com.civic.complaint.entity.ComplaintStatus;
import com.civic.complaint.entity.Priority;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface ComplaintRepository extends JpaRepository<Complaint, Long> {

    Optional<Complaint> findByTicketId(String ticketId);

    List<Complaint> findByCitizenIdOrderByCreatedAtDesc(Long citizenId);

    Page<Complaint> findByStatus(ComplaintStatus status, Pageable pageable);

    Page<Complaint> findByPriority(Priority priority, Pageable pageable);

    Page<Complaint> findByCategory(String category, Pageable pageable);

    @Query("SELECT c FROM Complaint c WHERE c.citizenId = :citizenId ORDER BY c.createdAt DESC")
    Page<Complaint> findByCitizenId(@Param("citizenId") Long citizenId, Pageable pageable);

    // Dashboard counts
    long countByStatus(ComplaintStatus status);
    long countByPriority(Priority priority);

    @Query("SELECT COUNT(c) FROM Complaint c WHERE c.status NOT IN ('RESOLVED', 'CLOSED')")
    long countOpenComplaints();

    @Query("SELECT COUNT(c) FROM Complaint c WHERE c.resolvedAt >= :since")
    long countResolvedSince(@Param("since") LocalDateTime since);

    // Search
    @Query("SELECT c FROM Complaint c WHERE " +
           "LOWER(c.description) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(c.ticketId) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(c.citizenName) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(c.category) LIKE LOWER(CONCAT('%', :search, '%')) OR " +
           "LOWER(c.topic) LIKE LOWER(CONCAT('%', :search, '%'))")
    Page<Complaint> searchComplaints(@Param("search") String search, Pageable pageable);

    // Analytics
    @Query("SELECT c.category, COUNT(c) FROM Complaint c WHERE c.category IS NOT NULL GROUP BY c.category")
    List<Object[]> countByCategory();

    @Query("SELECT c.priority, COUNT(c) FROM Complaint c WHERE c.priority IS NOT NULL GROUP BY c.priority")
    List<Object[]> countByPriorityGrouped();

    @Query("SELECT c.status, COUNT(c) FROM Complaint c GROUP BY c.status")
    List<Object[]> countByStatusGrouped();

    @Query("SELECT CAST(c.createdAt as LocalDate), COUNT(c) FROM Complaint c WHERE c.createdAt >= :since GROUP BY CAST(c.createdAt as LocalDate) ORDER BY CAST(c.createdAt as LocalDate)")
    List<Object[]> countByDateSince(@Param("since") LocalDateTime since);

    // Duplicate/recurring detection
    @Query("SELECT c FROM Complaint c WHERE c.category = :category AND c.address LIKE %:area% AND c.status NOT IN ('RESOLVED', 'CLOSED')")
    List<Complaint> findSimilarByAreaAndCategory(@Param("category") String category, @Param("area") String area);

    // Escalation candidates
    @Query("SELECT c FROM Complaint c WHERE c.slaDeadline < :now AND c.status NOT IN ('RESOLVED', 'CLOSED')")
    List<Complaint> findSlaBreached(@Param("now") LocalDateTime now);

    // Recent complaints for dashboard
    List<Complaint> findTop10ByOrderByCreatedAtDesc();

    // Critical alerts
    List<Complaint> findByPriorityAndStatusNotIn(Priority priority, List<ComplaintStatus> excludedStatuses);
}
