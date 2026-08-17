# Project Rules - Personal Fitness Tracker (FitTrack)

## Guidelines for Creating Projects

1. **Analyze Requirements**: Understand the task and set clear, achievable goals.
2. **Set Up Necessary Files**: Create the required directory structure and files.
3. **Implement Main Functionality**: Write the core code for the project.
4. **Handle Edge Cases**: Consider and handle potential errors or edge cases.
5. **Test the Implementation**: Run a simple test to verify the code works correctly.
6. **Verify Results**: Ensure the final output meets the requirements.

## Successful Implementations

- **To-do App (CLI)**: A simple to-do app in Python with functionalities for adding, viewing, and deleting tasks.
- **To-do App (Streamlit UI)**: A Streamlit UI for the to-do app with functionalities for adding, viewing, and deleting tasks.
- **To-do App (ChromaDB)**: A Streamlit UI for the to-do app using ChromaDB for persistent storage.
- **To-do App (AI Agent)**: An enhanced Streamlit UI with an AI agent that recommends tasks, provides insights, and analyzes task patterns.
- **To-do App (Deployment Ready)**: The app is prepared for free hosting with `requirements.txt` and `README.md` containing deployment instructions.
- **To-do App (GitHub Deployed)**: The app has been pushed to GitHub and is being deployed to Streamlit Community Cloud.
- **HomeChat (PRD Created)**: Product Requirements Document created for home level messaging and image hosting app.
- **HomeChat (App Implemented)**: Streamlit app with messaging and image upload functionality created.
- **HomeChat (Tests Passing)**: All module import, chat functionality, and Cloudinary structure tests pass.
- **HomeChat (GitHub Pushed)**: The app has been pushed to GitHub as a private repo (`sameer33337/homechat`).
- **FitTrack (PRD Created)**: Product Requirements Document created for personal fitness tracker.
- **FitTrack (Project Structure)**: Project folder created with prd.md, memory.md, and rules.md.
- **FitTrack (Data Source Analyzed)**: 4-week workout plan data received in JSON format and documented in PRD.
- **FitTrack (Tech Stack Decided)**: Web-first approach selected (React/Angular + Streamlit), iOS native hooks ready.
- **FitTrack (GitHub Pushed)**: The app has been pushed to GitHub as a private repo (`sameer33337/fitness-tracker`).

## Pending Tasks

### FitTrack - Next Steps

1. **Set Up Web App (PENDING)**:
   - Create React/Angular frontend
   - Create FastAPI backend
   - Set up Streamlit hosting
   - Create workout_plan.json with the 4-week data

2. **Implement Core Features (PENDING)**:
   - Data models (Exercise, WorkoutPlan, WorkoutLog)
   - Workout plan display (4-week schedule)
   - Exercise logging UI
   - Daily workout view
   - History view
   - Progress tracking

3. **Deploy to Streamlit (PENDING)**:
   - Code is already on GitHub (`sameer33337/fitness-tracker`)
   - Connect to Streamlit Community Cloud
   - Share the public URL

### iOS Native (Future - Requires macOS)

When macOS/Xcode becomes available:
- Create SwiftUI app with same data models
- Consume the FastAPI REST endpoints
- Add iCloud sync
- Integrate Apple Health

### HomeChat - Paused

HomeChat development is paused. The following tasks remain:
- Create UI for running the app locally on iPhone (similar to Telegram)
- Deployment to cloud hosting
- Cloudinary API setup

## Failures

- **Image Reading Failure**: The current model cannot read images. The workout image (`sameer workout.jpeg`) could not be analyzed directly. Resolved by having the user provide the workout data in JSON format.

## Testing

Before completing any project, run a simple test file to verify the implementation. Update this file with the test results.

### Test Results (PENDING)

No tests have been run yet for the FitTrack project.

## Notes

- Always ensure the code is syntactically correct before running.
- Use appropriate error handling to manage edge cases.
- Keep the code clean and well-documented.
- **Web-first strategy**: React/Angular + FastAPI + Streamlit for immediate deployment.
- **iOS hooks ready**: API layer, JSON data models, separated business logic for future iOS migration.
- The app is designed for personal use (Sameer's fitness tracking).
- Offline-first approach with localStorage persistence.
- The 4-week workout plan is the primary data source.
- Progressive overload is a key feature (Week 1 → Week 4 progression).
- Two exercise types: bodyweight (reps only) and weighted (reps/sets).
- Streamlit for hosting, React/Angular for frontend, FastAPI for backend.
- Data models are JSON-compatible and Swift-mappable for iOS migration.

## File Structure

```
Project/fitness-tracker/
├── prd.md          # Product Requirements Document
├── memory.md       # Task memory and progress
├── rules.md        # Project rules and guidelines
├── README.md       # Project overview
├── .gitignore      # Git exclusions
├── app.py          # Streamlit entry point (to be created)
├── requirements.txt # Python dependencies (to be created)
├── frontend/       # React/Angular frontend (to be created)
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── services/          # API services
│   │   ├── models/            # Data models
│   │   └── App.jsx            # Main app
│   └── package.json
├── backend/        # FastAPI backend (to be created)
│   ├── main.py                # API endpoints
│   ├── models.py              # Data models
│   └── workout_plan.json      # The workout plan data
└── ios/            # iOS native hooks (future)
    ├── Models/                # Swift data models
    └── README.md              # iOS migration guide