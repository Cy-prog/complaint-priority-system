package com.civic.complaint.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PriorityOverrideDTO {

    @NotBlank(message = "New priority is required")
    private String newPriority;

    private Integer newScore;

    @NotBlank(message = "Override reason is required")
    private String reason;
}
