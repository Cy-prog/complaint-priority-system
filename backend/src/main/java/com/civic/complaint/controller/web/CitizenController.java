package com.civic.complaint.controller.web;

import com.civic.complaint.dto.ComplaintCreateDTO;
import com.civic.complaint.entity.Complaint;
import com.civic.complaint.entity.User;
import com.civic.complaint.repository.NotificationRepository;
import com.civic.complaint.repository.StatusHistoryRepository;
import com.civic.complaint.repository.UserRepository;
import com.civic.complaint.service.ComplaintService;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.List;

@Controller
@RequestMapping("/citizen")
public class CitizenController {

    private final ComplaintService complaintService;
    private final UserRepository userRepository;
    private final StatusHistoryRepository historyRepo;
    private final NotificationRepository notificationRepo;

    public CitizenController(ComplaintService complaintService, UserRepository userRepository,
                            StatusHistoryRepository historyRepo, NotificationRepository notificationRepo) {
        this.complaintService = complaintService;
        this.userRepository = userRepository;
        this.historyRepo = historyRepo;
        this.notificationRepo = notificationRepo;
    }

    @GetMapping("/home")
    public String home(Authentication auth, Model model) {
        if (auth != null) {
            User user = userRepository.findByUsername(auth.getName()).orElse(null);
            if (user != null) {
                model.addAttribute("user", user);
                List<Complaint> myComplaints = complaintService.getBycitizenId(user.getId());
                model.addAttribute("recentComplaints", myComplaints.stream().limit(5).toList());
                model.addAttribute("totalComplaints", myComplaints.size());
                long resolved = myComplaints.stream().filter(c -> c.getResolvedAt() != null).count();
                model.addAttribute("resolvedComplaints", resolved);
                model.addAttribute("unreadNotifications",
                    notificationRepo.countByUserIdAndIsReadFalse(user.getId()));
            }
        }
        return "citizen/home";
    }

    @GetMapping("/submit")
    public String submitForm(Model model) {
        model.addAttribute("complaint", new ComplaintCreateDTO());
        return "citizen/submit";
    }

    @PostMapping("/submit")
    public String submitComplaint(@ModelAttribute ComplaintCreateDTO dto,
                                  Authentication auth,
                                  RedirectAttributes redirect) {
        User user = (auth != null && auth.getName() != null)
                ? userRepository.findByUsername(auth.getName()).orElse(null)
                : null;
        Long citizenId = user != null ? user.getId() : null;
        String citizenName = user != null ? user.getFullName() : dto.getCitizenName();
        if (citizenName == null || citizenName.isBlank()) {
            citizenName = "Anonymous Citizen";
        }

        Complaint complaint = complaintService.createComplaint(dto, citizenId, citizenName);
        redirect.addFlashAttribute("ticketId", complaint.getTicketId());
        redirect.addFlashAttribute("message", "Complaint submitted successfully!");
        return "redirect:/citizen/complaint/" + complaint.getTicketId();
    }

    @GetMapping("/my-complaints")
    public String myComplaints(Authentication auth, Model model) {
        if (auth == null || auth.getName() == null) {
            return "redirect:/login";
        }
        User user = userRepository.findByUsername(auth.getName()).orElse(null);
        if (user != null) {
            List<Complaint> complaints = complaintService.getByCitizenId(user.getId());
            model.addAttribute("complaints", complaints);
            model.addAttribute("user", user);
        }
        return "citizen/my-complaints";
    }

    @GetMapping("/complaint/{ticketId}")
    public String complaintDetail(@PathVariable String ticketId, Authentication auth, Model model) {
        Complaint complaint = complaintService.getByTicketId(ticketId);

        // Security: Only allow citizen to view their own complaints (or admins)
        if (auth != null) {
            User user = userRepository.findByUsername(auth.getName()).orElse(null);
            if (user != null && user.getRole().name().equals("CITIZEN") &&
                !user.getId().equals(complaint.getCitizenId())) {
                return "redirect:/citizen/home";
            }
            model.addAttribute("user", user);
        }

        model.addAttribute("complaint", complaint);
        model.addAttribute("statusHistory",
            historyRepo.findByComplaintIdOrderByChangedAtDesc(complaint.getId()));
        return "citizen/detail";
    }

    @PostMapping("/complaint/{ticketId}/feedback")
    public String submitFeedback(@PathVariable String ticketId,
                                 @RequestParam int rating,
                                 @RequestParam(required = false) String feedback,
                                 RedirectAttributes redirect) {
        complaintService.submitCitizenFeedback(ticketId, rating, feedback);
        redirect.addFlashAttribute("message", "Thank you for your feedback!");
        return "redirect:/citizen/complaint/" + ticketId;
    }

    @GetMapping("/track")
    public String trackComplaint(@RequestParam(required = false) String ticketId, Model model) {
        if (ticketId != null && !ticketId.isBlank()) {
            try {
                Complaint complaint = complaintService.getByTicketId(ticketId.trim().toUpperCase());
                model.addAttribute("complaint", complaint);
                model.addAttribute("statusHistory",
                    historyRepo.findByComplaintIdOrderByChangedAtDesc(complaint.getId()));
            } catch (Exception e) {
                model.addAttribute("error", "Complaint not found: " + ticketId);
            }
        }
        return "citizen/track";
    }
}
