# J.A.R.V.I.S — Web App

---

## Project Structure

```
jarvis/
├── app.py              ← Flask backend (all API logic)
├── requirements.txt    ← Python dependencies
├── render.yaml         ← Render deployment config
├── custom_sites.txt    ← Auto-created when you teach Jarvis new sites
├── Openai/             ← Auto-created folder for AI task outputs
└── templates/
    └── index.html      ← Full frontend (Iron Man HUD UI)
```

---

## Features

| Feature            | How to use                                      |
| ------------------ | ----------------------------------------------- |
| Chat with Jarvis   | Type or click the MIC button and speak          |
| Open websites      | Say "Open YouTube" / "Open GitHub"              |
| Get the time       | Say "What's the time"                           |
| Get the date       | Say "What's the date"                           |
| AI one-shot task   | Say "Using artificial intelligence, explain..." |
| Teach a new site   | Say "Remember website"                          |
| Reset conversation | Say "Reset chat" or click the RESET button      |
| Voice output       | Jarvis speaks every reply aloud automatically   |

---
