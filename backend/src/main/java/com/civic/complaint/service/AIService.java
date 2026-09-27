package com.civic.complaint.service;

import com.civic.complaint.dto.AIAnalysisResponse;
import com.civic.complaint.exception.AIServiceException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

/**
 * REST client that communicates with the Flask AI microservice.
 */
@Service
@SuppressWarnings("null")
public class AIService {

    private static final Logger log = LoggerFactory.getLogger(AIService.class);

    private final WebClient webClient;
    private final int timeoutSeconds;

    public AIService(
            @Value("${app.ai-service.base-url}") String baseUrl,
            @Value("${app.ai-service.api-key}") String apiKey,
            @Value("${app.ai-service.timeout-seconds:30}") int timeoutSeconds) {
        this.webClient = WebClient.builder()
                .baseUrl(baseUrl)
                .defaultHeader("X-API-Key", apiKey)
                .build();
        this.timeoutSeconds = timeoutSeconds;
    }

    /**
     * Send complaint text to the AI service for analysis.
     */
    public AIAnalysisResponse analyzeComplaint(String topic, String description, String address) {
        Map<String, Object> body = new HashMap<>();
        body.put("topic", topic != null ? topic : "");
        body.put("description", description);
        body.put("address", address != null ? address : "");

        try {
            return webClient.post()
                    .uri("/ai/analyze")
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(body)
                    .retrieve()
                    .bodyToMono(AIAnalysisResponse.class)
                    .timeout(Duration.ofSeconds(timeoutSeconds))
                    .block();
        } catch (Exception e) {
            log.error("AI service analysis failed: {}", e.getMessage());
            throw new AIServiceException("AI service unavailable. Complaint saved; analysis pending.", e);
        }
    }

    /**
     * Trigger model retraining on the Flask service.
     */
    public Map<String, Object> triggerTraining() {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> result = webClient.post()
                    .uri("/ai/train")
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(120))
                    .block();
            return result;
        } catch (Exception e) {
            log.error("AI training trigger failed: {}", e.getMessage());
            throw new AIServiceException("Failed to trigger model training", e);
        }
    }

    /**
     * Get current model status from the Flask service.
     */
    public Map<String, Object> getModelStatus() {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> result = webClient.get()
                    .uri("/ai/model/status")
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(10))
                    .block();
            return result;
        } catch (Exception e) {
            log.warn("Failed to get AI model status: {}", e.getMessage());
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("status", "unavailable");
            fallback.put("message", "AI service not reachable");
            return fallback;
        }
    }

    /**
     * Get model metrics from the Flask service.
     */
    public Map<String, Object> getModelMetrics() {
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> result = webClient.get()
                    .uri("/ai/model/metrics")
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(10))
                    .block();
            return result;
        } catch (Exception e) {
            log.warn("Failed to get AI model metrics: {}", e.getMessage());
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("status", "unavailable");
            return fallback;
        }
    }

    /**
     * Check if the AI service is healthy.
     */
    public boolean isHealthy() {
        try {
            webClient.get()
                    .uri("/ai/health")
                    .retrieve()
                    .bodyToMono(String.class)
                    .timeout(Duration.ofSeconds(5))
                    .block();
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
