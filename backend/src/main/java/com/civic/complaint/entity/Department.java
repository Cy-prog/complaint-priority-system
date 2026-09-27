package com.civic.complaint.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "departments")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor
@Builder
public class Department {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String name;

    @Column(length = 500)
    private String description;

    @Column(name = "head_name", length = 100)
    private String headName;

    @Column(name = "contact_email")
    private String contactEmail;

    @Column(name = "is_active", nullable = false)
    @Builder.Default
    private Boolean isActive = true;

    public String getCode() {
        if (name == null || name.isBlank()) return "DEP";
        String[] words = name.trim().split("\\s+");
        if (words.length == 1) {
            return name.substring(0, Math.min(3, name.length())).toUpperCase();
        }
        StringBuilder sb = new StringBuilder();
        for (String w : words) {
            if (!w.isEmpty()) sb.append(Character.toUpperCase(w.charAt(0)));
        }
        return sb.toString();
    }

    public String getEmail() {
        return contactEmail != null ? contactEmail : "dept@civic.gov.in";
    }
}
