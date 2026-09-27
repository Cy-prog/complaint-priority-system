package com.civic.complaint.controller.web;

import com.civic.complaint.entity.User;
import com.civic.complaint.entity.Role;
import com.civic.complaint.dto.UserRegistrationDTO;
import com.civic.complaint.repository.UserRepository;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@SuppressWarnings("null")
public class AuthController {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public AuthController(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @GetMapping("/login")
    public String loginPage(@RequestParam(value = "error", required = false) String error,
                           @RequestParam(value = "logout", required = false) String logout,
                           Model model) {
        if (error != null) model.addAttribute("error", "Invalid username or password");
        if (logout != null) model.addAttribute("message", "You have been logged out");
        return "auth/login";
    }

    @GetMapping("/register")
    public String registerPage(Model model) {
        model.addAttribute("user", new UserRegistrationDTO());
        return "auth/register";
    }

    @PostMapping("/register")
    public String registerUser(@ModelAttribute UserRegistrationDTO dto, RedirectAttributes redirect) {
        if (userRepository.existsByUsername(dto.getUsername())) {
            redirect.addFlashAttribute("error", "Username already exists");
            return "redirect:/register";
        }
        if (userRepository.existsByEmail(dto.getEmail())) {
            redirect.addFlashAttribute("error", "Email already exists");
            return "redirect:/register";
        }

        User user = User.builder()
                .username(dto.getUsername())
                .email(dto.getEmail())
                .passwordHash(passwordEncoder.encode(dto.getPassword()))
                .fullName(dto.getFullName())
                .mobile(dto.getMobile())
                .role(Role.CITIZEN) // Citizens register themselves
                .build();

        userRepository.save(user);
        redirect.addFlashAttribute("message", "Registration successful! Please login.");
        return "redirect:/login";
    }

    @GetMapping("/dashboard")
    public String dashboard(Authentication auth) {
        // Route to appropriate dashboard based on role
        String role = auth.getAuthorities().iterator().next().getAuthority();
        return switch (role) {
            case "ROLE_ADMIN" -> "redirect:/admin/dashboard";
            case "ROLE_HIGHER_AUTHORITY" -> "redirect:/authority/dashboard";
            case "ROLE_CITIZEN" -> "redirect:/citizen/home";
            default -> "redirect:/citizen/home";
        };
    }
}
