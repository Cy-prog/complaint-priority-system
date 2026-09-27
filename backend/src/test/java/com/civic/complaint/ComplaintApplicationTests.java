package com.civic.complaint;

import com.civic.complaint.dto.ComplaintCreateDTO;
import com.civic.complaint.entity.*;
import com.civic.complaint.repository.*;
import com.civic.complaint.service.AnalyticsService;
import com.civic.complaint.service.ComplaintService;
import com.civic.complaint.util.TicketIdGenerator;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
@ActiveProfiles("test")
@Transactional
class ComplaintApplicationTests {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private DepartmentRepository departmentRepository;

    @Autowired
    private CategoryRepository categoryRepository;

    @Autowired
    private ComplaintRepository complaintRepository;

    @Autowired
    private ComplaintService complaintService;

    @Autowired
    private AnalyticsService analyticsService;

    @Autowired
    private TicketIdGenerator ticketIdGenerator;

    @Test
    @DisplayName("Verify Spring Context Loads & Seed Data Exists")
    void contextLoadsAndSeedingVerified() {
        assertNotNull(userRepository);
        assertNotNull(departmentRepository);
        assertNotNull(categoryRepository);

        // Verify seeded users
        assertTrue(userRepository.findByUsername("admin").isPresent(), "Admin user should exist");
        assertTrue(userRepository.findByUsername("citizen").isPresent(), "Citizen user should exist");
        assertTrue(userRepository.findByUsername("authority").isPresent(), "Higher Authority user should exist");

        // Verify departments
        List<Department> depts = departmentRepository.findAll();
        assertFalse(depts.isEmpty(), "Municipal departments should be seeded");

        // Verify categories
        List<Category> categories = categoryRepository.findAll();
        assertFalse(categories.isEmpty(), "Categories should be seeded");

        // Verify complaints
        assertFalse(complaintRepository.findAll().isEmpty(), "Complaints should be seeded");
    }

    @Test
    @DisplayName("Verify Ticket ID Format (GWA-XXXX)")
    void testTicketIdGeneration() {
        String ticketId = ticketIdGenerator.generate();
        assertNotNull(ticketId);
        assertTrue(ticketId.startsWith("GWA-"), "Ticket ID must start with GWA- prefix");
        assertEquals(8, ticketId.length(), "Ticket ID should be GWA-XXXX (8 chars)");
    }

    @Test
    @DisplayName("Verify Complaint Creation & Lifecycle Transitions")
    void testComplaintCreationAndLifecycle() {
        User citizen = userRepository.findByUsername("citizen").orElseThrow();

        ComplaintCreateDTO dto = ComplaintCreateDTO.builder()
                .topic("Broken Streetlight")
                .description("Streetlight pole broken and dark street near park for 3 days")
                .address("Sector 4 Park Road, City")
                .latitude(28.6139)
                .longitude(77.2090)
                .build();

        Complaint created = complaintService.createComplaint(dto, citizen.getId(), citizen.getFullName());

        assertNotNull(created.getId());
        assertNotNull(created.getTicketId());
        assertTrue(created.getTicketId().startsWith("GWA-"));
        assertTrue(created.getStatus() == ComplaintStatus.SUBMITTED || created.getStatus() == ComplaintStatus.AI_ANALYSIS_PENDING,
                "Status should be SUBMITTED or AI_ANALYSIS_PENDING");

        // Test Priority Override & SLA Deadline Generation
        complaintService.overridePriority(
                created.getTicketId(),
                com.civic.complaint.dto.PriorityOverrideDTO.builder()
                        .newPriority("HIGH")
                        .reason("Urgent street light hazard near school")
                        .build(),
                1L,
                "admin"
        );
        Complaint updatedPrio = complaintService.getByTicketId(created.getTicketId());
        assertEquals(Priority.HIGH, updatedPrio.getPriority());
        assertNotNull(updatedPrio.getSlaDeadline(), "SLA deadline should be set after priority is assigned");

        // Test Second Consecutive Priority Override (verifies no unique constraint violation on SLARecord)
        complaintService.overridePriority(
                created.getTicketId(),
                com.civic.complaint.dto.PriorityOverrideDTO.builder()
                        .newPriority("CRITICAL")
                        .reason("Further escalation: sparked near kindergarten")
                        .build(),
                1L,
                "admin"
        );
        Complaint criticalPrio = complaintService.getByTicketId(created.getTicketId());
        assertEquals(Priority.CRITICAL, criticalPrio.getPriority());

        // Test nonexistent ticket ID handling
        assertThrows(com.civic.complaint.exception.ResourceNotFoundException.class, () -> {
            complaintService.getByTicketId("GWA-NONEXISTENT-999");
        });

        // Test Status Transition to IN_PROGRESS
        Complaint inProgress = complaintService.updateStatus(
                created.getTicketId(),
                ComplaintStatus.IN_PROGRESS,
                1L,
                "admin",
                "Field maintenance team assigned"
        );
        assertEquals(ComplaintStatus.IN_PROGRESS, inProgress.getStatus());

        // Test Status Transition to RESOLVED
        Complaint resolved = complaintService.updateStatus(
                created.getTicketId(),
                ComplaintStatus.RESOLVED,
                1L,
                "admin",
                "Light bulb and wire replaced successfully"
        );
        assertEquals(ComplaintStatus.RESOLVED, resolved.getStatus());
        assertNotNull(resolved.getResolvedAt());
    }

    @Test
    @DisplayName("Verify Dashboard Analytics & Trend Queries")
    void testDashboardAndAnalyticsQueries() {
        // 1. Dashboard summary
        var summary = analyticsService.getDashboardSummary();
        assertNotNull(summary);
        assertTrue(summary.getTotalComplaints() >= 5);

        // 2. Category distribution
        List<Map<String, Object>> catDist = analyticsService.getCategoryDistribution();
        assertNotNull(catDist);
        assertFalse(catDist.isEmpty());

        // 3. Priority distribution
        List<Map<String, Object>> prioDist = analyticsService.getPriorityDistribution();
        assertNotNull(prioDist);
        assertFalse(prioDist.isEmpty());

        // 4. Status distribution
        List<Map<String, Object>> statusDist = analyticsService.getStatusDistribution();
        assertNotNull(statusDist);
        assertFalse(statusDist.isEmpty());

        // 5. Complaints trend (previously failing with Function DATE not found)
        List<Map<String, Object>> trend = analyticsService.getComplaintsTrend(30);
        assertNotNull(trend);
        assertFalse(trend.isEmpty(), "Complaints trend should return daily aggregated counts");
        for (Map<String, Object> point : trend) {
            assertNotNull(point.get("date"), "Date key must be present in trend");
            assertNotNull(point.get("count"), "Count key must be present in trend");
        }

        // 6. Direct repository countByDateSince query
        List<Object[]> rows = complaintRepository.countByDateSince(LocalDateTime.now().minusDays(30));
        assertNotNull(rows);
        assertFalse(rows.isEmpty());
        Object firstDate = rows.get(0)[0];
        assertNotNull(firstDate);
    }
}
