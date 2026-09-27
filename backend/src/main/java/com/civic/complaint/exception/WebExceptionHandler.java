package com.civic.complaint.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import jakarta.servlet.http.HttpServletRequest;

@ControllerAdvice(basePackages = "com.civic.complaint.controller.web")
public class WebExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(WebExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public String handleResourceNotFound(ResourceNotFoundException ex, HttpServletRequest request, RedirectAttributes redirect, Model model) {
        log.warn("Web resource not found: {} for URI: {}", ex.getMessage(), request.getRequestURI());
        String uri = request.getRequestURI();
        if (uri.startsWith("/admin")) {
            redirect.addFlashAttribute("error", ex.getMessage());
            return "redirect:/admin/dashboard";
        } else if (uri.startsWith("/authority")) {
            redirect.addFlashAttribute("error", ex.getMessage());
            return "redirect:/authority/dashboard";
        } else {
            redirect.addFlashAttribute("error", ex.getMessage());
            return "redirect:/citizen/home";
        }
    }

    @ExceptionHandler(AccessDeniedException.class)
    public String handleAccessDenied(AccessDeniedException ex, HttpServletRequest request, RedirectAttributes redirect) {
        log.warn("Access denied for URI {}: {}", request.getRequestURI(), ex.getMessage());
        redirect.addFlashAttribute("error", "Access Denied: You do not have permission to view that resource.");
        return "redirect:/dashboard";
    }

    @ExceptionHandler(Exception.class)
    public String handleGeneralWebError(Exception ex, HttpServletRequest request, Model model) {
        log.error("Unhandled web exception on URI {}: ", request.getRequestURI(), ex);
        model.addAttribute("errorMessage", ex.getMessage() != null ? ex.getMessage() : "An unexpected error occurred");
        model.addAttribute("requestUri", request.getRequestURI());
        return "error";
    }
}
