package com.civic.complaint.util;

import org.springframework.stereotype.Component;
import java.security.SecureRandom;

/**
 * Generates unique ticket IDs in the format GWA-XXXX.
 */
@Component
public class TicketIdGenerator {

    private static final String PREFIX = "GWA";
    private static final SecureRandom random = new SecureRandom();

    public String generate() {
        int num = 1000 + random.nextInt(9000); // 4-digit number: 1000-9999
        return PREFIX + "-" + num;
    }

    public String generateWithSuffix() {
        int num = 1000 + random.nextInt(9000);
        char suffix = (char) ('A' + random.nextInt(26));
        return PREFIX + "-" + num + suffix;
    }
}
