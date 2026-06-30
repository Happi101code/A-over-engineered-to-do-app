@echo off
cd Backend
call venv\Scripts\activate
start cmd /k uvicorn main:app --reload
cd ..\Frontend
start http://localhost:3000