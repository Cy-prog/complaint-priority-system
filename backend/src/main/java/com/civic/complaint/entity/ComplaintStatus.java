package com.civic.complaint.entity;

/**
 * Complaint lifecycle statuses.
 */
public enum ComplaintStatus {
    SUBMITTED,
    AI_ANALYSIS_PENDING,
    CLASSIFIED,
    ASSIGNED,
    IN_PROGRESS,
    ESCALATED,
    RESOLVED,
    CITIZEN_FEEDBACK,
    CLOSED,
    REOPENED
}
