---
description: How to run the FarmDoctor AI project (Backend + Frontend)
---

To run the entire FarmDoctor AI project with one command and ensure both services are monitored:

// turbo
1. Run the startup script:
```powershell
python start_all.py
```

This script will:
- Start the FastAPI Backend on port 8000.
- Start the Streamlit Frontend.
- Automatically restart them if they crash.
- Allow you to stop both easily with `Ctrl+C`.

Alternatively, if you want to run them manually:

1. Start the Backend:
```powershell
cd Backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Start the Frontend (in a new terminal):
```powershell
streamlit run Backend/Frontend/app.py
```
