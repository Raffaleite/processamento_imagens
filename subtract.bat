@echo off
cd /d %~dp0
python main.py --subtract imagens\fundo.jpg imagens\frente.jpg
pause
