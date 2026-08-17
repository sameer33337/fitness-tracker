# FitTrack - Personal Fitness Tracker

A web-based fitness tracker to digitize the 4-week progressive workout plan. Log exercises, sets, reps, and weights, track weekly progression, and monitor personal records. Architecture designed with iOS native hooks ready for future migration.

## Overview

FitTrack is a personal fitness tracking app designed to replace the hand-drawn 4-week workout plan. It provides an intuitive interface for viewing the weekly schedule, logging completed exercises, and tracking progressive overload across weeks.

**Strategy**: Web-first (React/Angular + Streamlit) for immediate deployment, with iOS native hooks ready for future migration to macOS/Xcode.

## Features

- **4-Week Workout Plan**: Display the full weekly schedule (Monday-Sunday)
- **Exercise Logging**: Log completed exercises with sets, reps, and weights
- **Two Exercise Types**: Bodyweight (reps only) and Weighted (reps/sets)
- **Progressive Overload**: Track weekly progression (Week 1 → Week 4)
- **Cardio Tracking**: Log daily cardio sessions (10-15 min)
- **History View**: Browse past workout sessions by date
- **Progress Charts**: Visualize weight/reps progression over time
- **Personal Records**: Automatically track personal bests
- **Offline-first**: Data stored in browser localStorage
- **iOS-Ready**: API layer and JSON data models for future native app

## Workout Plan

The app is based on a 4-week progressive workout program:

| Week | Cardio | Progression |
|------|--------|-------------|
| **Week 1** | 10 Min | Base exercises |
| **Week 2** | 10 Min | Repeats Week 1 with increases |
| **Week 3** | 15 Min | Repeats Week 2 +1 rep |
| **Week 4** | 15 Min | Repeats Week 3 +5 reps +1 set |

### Exercise Format
- **Bodyweight**: `[reps] [Exercise]` (e.g., "25 Pullups")
- **Weighted**: `[reps]/[sets] [Exercise]` (e.g., "15/4 Bicep Curl" = 15 reps, 4 sets)

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | React (or Angular) |
| **Backend** | Python FastAPI |
| **Hosting** | Streamlit |
| **Data Persistence** | Browser localStorage + JSON |
| **Charts** | Chart.js / Recharts |
| **Architecture** | Component-based + API layer |

## iOS Native Hooks

The project is designed with iOS native migration in mind:
- **API layer**: RESTful API endpoints that can be consumed by iOS app
- **Data models**: JSON-compatible data structures that map to Swift models
- **Business logic**: Separated from UI for reuse
- **Auth-ready**: API authentication hooks for future multi-device sync

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deployment

1. Push code to GitHub
2. Connect to Streamlit Community Cloud
3. Share the public URL

## Project Structure

```
Project/fitness-tracker/
├── prd.md          # Product Requirements Document
├── memory.md       # Task memory and progress
├── rules.md        # Project rules and guidelines
├── README.md       # This file
├── .gitignore      # Git exclusions
├── app.py          # Streamlit entry point
├── requirements.txt # Python dependencies
├── frontend/       # React/Angular frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── services/          # API services
│   │   ├── models/            # Data models
│   │   └── App.jsx            # Main app
│   └── package.json
├── backend/        # FastAPI backend
│   ├── main.py                # API endpoints
│   ├── models.py              # Data models
│   └── workout_plan.json      # The workout plan data
└── ios/            # iOS native hooks (future)
    ├── Models/                # Swift data models
    └── README.md              # iOS migration guide
```

## Status

**Planning Phase** - Project structure, PRD, and workout plan data documented. Web app development pending.

## License

Private - Personal use