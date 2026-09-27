package com.civic.complaint.config;

import com.civic.complaint.service.CustomUserDetailsService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    private final CustomUserDetailsService userDetailsService;

    public SecurityConfig(CustomUserDetailsService userDetailsService) {
        this.userDetailsService = userDetailsService;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                // Public pages
                .requestMatchers("/", "/login", "/register", "/css/**", "/js/**", "/images/**",
                    "/favicon.ico", "/h2-console/**", "/error").permitAll()
                // Public citizen portal pages
                .requestMatchers("/citizen/home", "/citizen/submit", "/citizen/track").permitAll()
                // Public API endpoints
                .requestMatchers("/api/auth/**", "/api/health", "/api/categories").permitAll()
                // Citizen endpoints — require CITIZEN or higher
                .requestMatchers("/citizen/**").hasAnyRole("CITIZEN", "ADMIN", "HIGHER_AUTHORITY")
                .requestMatchers("/api/complaints/my/**").hasAnyRole("CITIZEN", "ADMIN", "HIGHER_AUTHORITY")
                // Admin endpoints
                .requestMatchers("/admin/**").hasAnyRole("ADMIN", "HIGHER_AUTHORITY")
                .requestMatchers("/api/admin/**").hasAnyRole("ADMIN", "HIGHER_AUTHORITY")
                // Higher authority endpoints
                .requestMatchers("/authority/**").hasRole("HIGHER_AUTHORITY")
                .requestMatchers("/api/higher/**").hasRole("HIGHER_AUTHORITY")
                // AI management — admin only
                .requestMatchers("/api/ai/train", "/api/ai/model/retrain", "/api/ai/model/deploy").hasRole("ADMIN")
                // Everything else requires auth
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .loginProcessingUrl("/login")
                .defaultSuccessUrl("/dashboard", true)
                .failureUrl("/login?error=true")
                .permitAll()
            )
            .logout(logout -> logout
                .logoutUrl("/logout")
                .logoutSuccessUrl("/login?logout=true")
                .invalidateHttpSession(true)
                .deleteCookies("JSESSIONID")
                .permitAll()
            )
            .sessionManagement(session -> session
                .maximumSessions(1)
                .maxSessionsPreventsLogin(false)
            )
            .csrf(csrf -> csrf
                .ignoringRequestMatchers("/api/**", "/h2-console/**")
            )
            .headers(headers -> headers
                .frameOptions(frame -> frame.sameOrigin())  // for H2 console
            )
            .userDetailsService(userDetailsService);

        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
}
