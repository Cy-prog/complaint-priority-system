package com.civic.complaint.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ComplaintCreateDTO {

    private String citizenName;
    private String mobile;
    private String topic;

    @NotBlank(message = "Complaint description is required")
    @Size(min = 10, max = 5000, message = "Description must be between 10 and 5000 characters")
    private String description;

    private String address;
    private Double latitude;
    private Double longitude;
}
