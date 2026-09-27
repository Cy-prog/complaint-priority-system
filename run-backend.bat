@echo off
echo ===================================================
echo Starting CivicPulse Backend (Spring Boot: 8080)...
echo ===================================================
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot
cd backend
call mvnw.cmd spring-boot:run
pause
