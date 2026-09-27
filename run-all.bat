@echo off
echo ===================================================
echo Launching AI-Based Complaint Prioritization Platform
echo ===================================================
echo 1. Starting AI Microservice (Flask :5000)...
start "CivicPulse AI Service" cmd /k "run-ai-service.bat"

echo 2. Waiting 3 seconds before starting Backend...
timeout /t 3 /nobreak >nul

echo 3. Starting Spring Boot Backend (:8080)...
start "CivicPulse Backend" cmd /k "run-backend.bat"

echo ===================================================
echo Platform launched!
echo Web Portal: http://localhost:8080
echo Admin: admin / admin123
echo Authority: authority / authority123
echo Citizen: citizen / citizen123
echo ===================================================
pause
