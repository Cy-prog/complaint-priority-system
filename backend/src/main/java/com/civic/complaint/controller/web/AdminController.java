package com.civic.complaint.controller.web;

import com.civic.complaint.dto.DashboardDTO;
import com.civic.complaint.dto.PriorityOverrideDTO;
import com.civic.complaint.entity.*;
import com.civic.complaint.repository.*;
import com.civic.complaint.service.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/admin")
@SuppressWarnings("null")
public class AdminController {

    private final ComplaintService complaintService;
    private final AnalyticsService analyticsService;
    private final AIService aiService;
    private final UserRepository userRepo;
    private final DepartmentRepository deptRepo;
    private final CategoryRepository catRepo;
    private final ComplaintRepository complaintRepo;
    private final StatusHistoryRepository historyRepo;
    private final PriorityOverrideRepository overrideRepo;
    private final AuditLogRepository auditRepo;
    private final NotificationRepository notificationRepo;

    public AdminController(ComplaintService complaintService, AnalyticsService analyticsService,
                          AIService aiService, UserRepository userRepo,
                          DepartmentRepository deptRepo, CategoryRepository catRepo,
                          ComplaintRepository complaintRepo, StatusHistoryRepository historyRepo,
                          PriorityOverrideRepository overrideRepo, AuditLogRepository auditRepo,
                          NotificationRepository notificationRepo) {
        this.complaintService = complaintService;
        this.analyticsService = analyticsService;
        this.aiService = aiService;
        this.userRepo = userRepo;
        this.deptRepo = deptRepo;
        this.catRepo = catRepo;
        this.complaintRepo = complaintRepo;
        this.historyRepo = historyRepo;
        this.overrideRepo = overrideRepo;
        this.auditRepo = auditRepo;
        this.notificationRepo = notificationRepo;
    }

    private String getUsername(Authentication auth) {
        return (auth != null && auth.getName() != null) ? auth.getName() : "admin";
    }

    private User getUser(Authentication auth) {
        return userRepo.findByUsername(getUsername(auth)).orElse(null);
    }

    @GetMapping("/dashboard")
    public String dashboard(Authentication auth, Model model) {
        User user = getUser(auth);
        DashboardDTO summary = analyticsService.getDashboardSummary();
        List<Complaint> recent = complaintService.getRecent();
        List<Complaint> criticalAlerts = complaintRepo.findByPriorityAndStatusNotIn(
            Priority.CRITICAL, List.of(ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED));

        model.addAttribute("user", user);
        model.addAttribute("summary", summary);
        model.addAttribute("recentComplaints", recent);
        model.addAttribute("criticalAlerts", criticalAlerts);
        model.addAttribute("categoryDistribution", analyticsService.getCategoryDistribution());
        model.addAttribute("priorityDistribution", analyticsService.getPriorityDistribution());
        model.addAttribute("complaintsTrend", analyticsService.getComplaintsTrend(30));

        if (user != null) {
            model.addAttribute("unreadNotifications",
                notificationRepo.countByUserIdAndIsReadFalse(user.getId()));
        }
        return "admin/dashboard";
    }

    @GetMapping("/complaints")
    public String complaints(@RequestParam(defaultValue = "0") int page,
                            @RequestParam(defaultValue = "") String search,
                            @RequestParam(required = false) String status,
                            @RequestParam(required = false) String priority,
                            Authentication auth, Model model) {
        User user = getUser(auth);
        PageRequest pageable = PageRequest.of(page, 20, Sort.by("createdAt").descending());

        Page<Complaint> complaints;
        if (!search.isBlank()) {
            complaints = complaintService.search(search.trim(), pageable);
        } else if (status != null && !status.isBlank()) {
            try {
                complaints = complaintService.getByStatus(ComplaintStatus.valueOf(status.trim().toUpperCase()), pageable);
            } catch (IllegalArgumentException e) {
                complaints = complaintService.listAll(pageable);
            }
        } else if (priority != null && !priority.isBlank()) {
            try {
                complaints = complaintService.getByPriority(Priority.valueOf(priority.trim().toUpperCase()), pageable);
            } catch (IllegalArgumentException e) {
                complaints = complaintService.listAll(pageable);
            }
        } else {
            complaints = complaintService.listAll(pageable);
        }

        model.addAttribute("user", user);
        model.addAttribute("complaints", complaints);
        model.addAttribute("search", search);
        model.addAttribute("selectedStatus", status);
        model.addAttribute("selectedPriority", priority);
        model.addAttribute("departments", deptRepo.findAll());
        model.addAttribute("categories", catRepo.findAll());
        return "admin/complaints";
    }

    @GetMapping("/complaint/{ticketId}")
    public String complaintDetail(@PathVariable String ticketId, Authentication auth, Model model, RedirectAttributes redirect) {
        String username = (auth != null && auth.getName() != null) ? auth.getName() : "admin";
        User user = userRepo.findByUsername(username).orElse(null);

        Complaint complaint;
        try {
            complaint = complaintService.getByTicketId(ticketId);
        } catch (Exception e) {
            redirect.addFlashAttribute("error", "Complaint not found: " + ticketId);
            return "redirect:/admin/complaints";
        }

        model.addAttribute("user", user);
        model.addAttribute("complaint", complaint);
        model.addAttribute("statusHistory",
            historyRepo.findByComplaintIdOrderByChangedAtDesc(complaint.getId()));
        model.addAttribute("overrides",
            overrideRepo.findByComplaintIdOrderByChangedAtDesc(complaint.getId()));
        model.addAttribute("departments", deptRepo.findAll());
        model.addAttribute("categories", catRepo.findAll());
        model.addAttribute("aiHealthy", aiService.isHealthy());
        return "admin/complaint-detail";
    }

    @GetMapping("/complaint/{ticketId}/override")
    public String overridePriorityGet(@PathVariable String ticketId) {
        return "redirect:/admin/complaint/" + ticketId;
    }

    @PostMapping("/complaint/{ticketId}/status")
    public String updateStatus(@PathVariable String ticketId,
                              @RequestParam String newStatus,
                              @RequestParam(required = false) String note,
                              Authentication auth,
                              RedirectAttributes redirect) {
        String username = (auth != null && auth.getName() != null) ? auth.getName() : "admin";
        User user = userRepo.findByUsername(username).orElse(null);
        try {
            complaintService.updateStatus(ticketId, ComplaintStatus.valueOf(newStatus),
                user != null ? user.getId() : 1L, username, note);
            redirect.addFlashAttribute("message", "Status updated to " + newStatus);
        } catch (Exception e) {
            redirect.addFlashAttribute("error", "Status update failed: " + e.getMessage());
        }
        return "redirect:/admin/complaint/" + ticketId;
    }

    @PostMapping("/complaint/{ticketId}/assign")
    public String assignComplaint(@PathVariable String ticketId,
                                  @RequestParam Long departmentId,
                                  @RequestParam(required = false) String officer,
                                  Authentication auth,
                                  RedirectAttributes redirect) {
        String username = (auth != null && auth.getName() != null) ? auth.getName() : "admin";
        User user = userRepo.findByUsername(username).orElse(null);
        Department dept = deptRepo.findById(departmentId).orElse(null);
        if (dept != null) {
            try {
                complaintService.assignComplaint(ticketId, dept, officer, null,
                    user != null ? user.getId() : 1L, username);
                redirect.addFlashAttribute("message", "Assigned to " + dept.getName());
            } catch (Exception e) {
                redirect.addFlashAttribute("error", "Assignment failed: " + e.getMessage());
            }
        } else {
            redirect.addFlashAttribute("error", "Department not found");
        }
        return "redirect:/admin/complaint/" + ticketId;
    }

    @PostMapping("/complaint/{ticketId}/override")
    public String overridePriority(@PathVariable String ticketId,
                                   @ModelAttribute PriorityOverrideDTO dto,
                                   Authentication auth,
                                   RedirectAttributes redirect) {
        String username = (auth != null && auth.getName() != null) ? auth.getName() : "admin";
        User user = userRepo.findByUsername(username).orElse(null);
        Long userId = (user != null) ? user.getId() : 1L;

        if (dto == null || dto.getNewPriority() == null || dto.getNewPriority().isBlank()) {
            redirect.addFlashAttribute("error", "Please select a valid priority.");
            return "redirect:/admin/complaint/" + ticketId;
        }

        try {
            complaintService.overridePriority(ticketId, dto, userId, username);
            redirect.addFlashAttribute("message", "Priority overridden to " + dto.getNewPriority());
        } catch (com.civic.complaint.exception.ResourceNotFoundException e) {
            redirect.addFlashAttribute("error", "Complaint not found: " + ticketId);
            return "redirect:/admin/complaints";
        } catch (Exception e) {
            redirect.addFlashAttribute("error", "Override failed: " + e.getMessage());
        }
        return "redirect:/admin/complaint/" + ticketId;
    }

    @PostMapping("/complaint/{ticketId}/reanalyze")
    public String reanalyze(@PathVariable String ticketId, RedirectAttributes redirect) {
        try {
            Complaint complaint = complaintService.getByTicketId(ticketId);
            complaintService.triggerAIAnalysis(complaint.getId());
            redirect.addFlashAttribute("message", "AI re-analysis triggered");
        } catch (Exception e) {
            redirect.addFlashAttribute("error", "Re-analysis failed: " + e.getMessage());
        }
        return "redirect:/admin/complaint/" + ticketId;
    }

    @GetMapping("/analytics")
    public String analytics(Authentication auth, Model model) {
        User user = getUser(auth);
        model.addAttribute("user", user);
        model.addAttribute("summary", analyticsService.getDashboardSummary());
        model.addAttribute("categoryDistribution", analyticsService.getCategoryDistribution());
        model.addAttribute("priorityDistribution", analyticsService.getPriorityDistribution());
        model.addAttribute("statusDistribution", analyticsService.getStatusDistribution());
        model.addAttribute("complaintsTrend", analyticsService.getComplaintsTrend(30));
        return "admin/analytics";
    }

    @GetMapping("/ai")
    public String aiDashboard(Authentication auth, Model model) {
        User user = getUser(auth);
        model.addAttribute("user", user);
        model.addAttribute("modelStatus", aiService.getModelStatus());
        model.addAttribute("modelMetrics", aiService.getModelMetrics());
        model.addAttribute("aiHealthy", aiService.isHealthy());
        model.addAttribute("summary", analyticsService.getDashboardSummary());
        return "admin/ai-intelligence";
    }

    @PostMapping("/ai/train")
    public String trainModel(RedirectAttributes redirect) {
        try {
            Map<String, Object> result = aiService.triggerTraining();
            redirect.addFlashAttribute("message", "Model training triggered: " + result.toString());
        } catch (Exception e) {
            redirect.addFlashAttribute("error", "Training failed: " + e.getMessage());
        }
        return "redirect:/admin/ai";
    }

    @GetMapping("/users")
    public String users(Authentication auth, Model model) {
        User user = getUser(auth);
        model.addAttribute("user", user);
        model.addAttribute("users", userRepo.findAll());
        return "admin/users";
    }

    @GetMapping("/audit")
    public String auditLogs(@RequestParam(defaultValue = "0") int page,
                           Authentication auth, Model model) {
        User user = getUser(auth);
        model.addAttribute("user", user);
        model.addAttribute("logs", auditRepo.findAllByOrderByCreatedAtDesc(
            PageRequest.of(page, 50)));
        return "admin/audit";
    }
}
