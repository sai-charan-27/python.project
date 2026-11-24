@echo off
title Weather Data Visualizer - CampusSolve Project #91
echo Starting Weather Data Visualizer...
cd /d "%~dp0Weather_Data_Visualizer"
py -3.13 main.py || python main.py
pause
