@echo off
cd Backend
call venv\Scripts\activate
start cmd /k uvicorn main:app --reload
cd ..\Frontend
python -m http.server 3000