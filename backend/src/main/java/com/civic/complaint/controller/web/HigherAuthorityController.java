package com.civic.complaint.controller.web;

import com.civic.complaint.entity.*;
import com.civic.complaint.repository.*;
import com.civic.complaint.service.*;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/authority")
public class HigherAuthorityController {

    private final AnalyticsService analyticsService;
    private final AIService aiService;
    private final UserRepository userRepo;
    private final ComplaintRepository complaintRepo;
    private final DepartmentRepository deptRepo;
    private final NotificationRepository notificationRepo;

    public HigherAuthorityController(AnalyticsService analyticsService,
                                     AIService aiService, UserRepository userRepo,
                                     ComplaintRepository complaintRepo, DepartmentRepository deptRepo,
                                     NotificationRepository notificationRepo) {
        this.analyticsService = analyticsService;
        this.aiService = aiService;
        this.userRepo = userRepo;
        this.complaintRepo = complaintRepo;
        this.deptRepo = deptRepo;
        this.notificationRepo = notificationRepo;
    }

    @GetMapping("/dashboard")
    public String dashboard(Authentication auth, Model model) {
        String username = (auth != null && auth.getName() != null) ? auth.getName() : "authority";
        User user = userRepo.findByUsername(username).orElse(null);

        model.addAttribute("user", user);
        model.addAttribute("summary", analyticsService.getDashboardSummary());
        model.addAttribute("categoryDistribution", analyticsService.getCategoryDistribution());
        model.addAttribute("priorityDistribution", analyticsService.getPriorityDistribution());
        model.addAttribute("statusDistribution", analyticsService.getStatusDistribution());
        model.addAttribute("complaintsTrend", analyticsService.getComplaintsTrend(30));
        model.addAttribute("departments", deptRepo.findAll());

        // Critical unresolved
        List<Complaint> critical = complaintRepo.findByPriorityAndStatusNotIn(
            Priority.CRITICAL, List.of(ComplaintStatus.RESOLVED, ComplaintStatus.CLOSED));
        model.addAttribute("criticalComplaints", critical);

        // SLA breached
        List<Complaint> slaBreached = complaintRepo.findSlaBreached(java.time.LocalDateTime.now());
        model.addAttribute("slaBreached", slaBreached);

        // AI status
        model.addAttribute("modelStatus", aiService.getModelStatus());
        model.addAttribute("modelMetrics", aiService.getModelMetrics());

        if (user != null) {
            model.addAttribute("unreadNotifications",
                notificationRepo.countByUserIdAndIsReadFalse(user.getId()));
        }

        return "authority/dashboard";
    }

    @GetMapping("/departments")
    public String departments(Authentication auth, Model model) {
        User user = userRepo.findByUsername(auth.getName()).orElse(null);
        model.addAttribute("user", user);
        model.addAttribute("departments", deptRepo.findAll());
        model.addAttribute("categoryDistribution", analyticsService.getCategoryDistribution());
        return "authority/departments";
    }

    @GetMapping("/reports")
    public String reports(Authentication auth, Model model) {
        User user = userRepo.findByUsername(auth.getName()).orElse(null);
        model.addAttribute("user", user);
        model.addAttribute("summary", analyticsService.getDashboardSummary());
        model.addAttribute("complaintsTrend", analyticsService.getComplaintsTrend(90));
        return "authority/reports";
    }
}
