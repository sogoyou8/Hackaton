@echo off
title TechCorp AI Chat Launcher
echo ===================================================
echo   TechCorp AI Chat - Lanceur Automatique Securise
echo ===================================================
echo.

echo [*] Preparation de l'environnement Ollama...
echo [*] Fermeture des instances existantes d'Ollama...
taskkill /f /im ollama.exe >nul 2>&1
taskkill /f /im "ollama app.exe" >nul 2>&1

echo [*] Activation des autorisations CORS...
set OLLAMA_ORIGINS=*

echo [*] Demarrage du serveur Ollama en arriere-plan...
start /b ollama serve >nul 2>&1

echo [*] Attente du demarrage d'Ollama (5 secondes)...
timeout /t 5 /nobreak >nul

echo [*] Lancement de l'interface de chat dans le navigateur...
start index.html

echo.
echo ===================================================
echo  [+] Chatbot lance avec succes !
echo  [!] Laissez cette fenetre ouverte pendant le chat.
echo ===================================================
echo.
pause
