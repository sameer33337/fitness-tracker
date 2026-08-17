# Task Memory - Personal Fitness Tracker

## Project Status: FitTrack - Web App (iOS-Ready)

- [x] Analyze requirements
- [x] Set up project structure (prd.md, memory.md, rules.md)
- [x] Analyze workout data source (JSON provided by user)
- [x] Decide tech stack: Web-first (React/Angular + Streamlit), iOS native later
- [x] Push project to GitHub (private repo: `sameer33337/fitness-tracker`)
- [ ] Set up web app (React/Angular + FastAPI + Streamlit)
- [ ] Implement data models
- [ ] Implement workout plan display
- [ ] Implement workout logging UI
- [ ] Implement history view
- [ ] Implement progress tracking
- [ ] Test the implementation
- [ ] Verify results

## Project Location

- **Project Directory**: `Project/fitness-tracker/`
- **PRD Document**: `Project/fitness-tracker/prd.md`
- **Memory File**: `Project/fitness-tracker/memory.md`
- **Rules File**: `Project/fitness-tracker/rules.md`
- **GitHub Repo**: `https://github.com/sameer33337/fitness-tracker` (private)
- **Source Image**: `C:\Users\91903\Downloads\sameer workout.jpeg`
- **Source PDF**: `C:\Users\91903\Downloads\sameer workout.pdf`

## Implementation Summary

The FitTrack app is a personal fitness tracker that digitizes the user's 4-week workout plan. **Strategy: Web-first** - build with React/Angular + Streamlit for web, with iOS native hooks ready for future migration to macOS/Xcode.

### Tech Stack Decision (2026-08-17)

**Decision**: Build web-first with React/Angular + FastAPI + Streamlit, scale to iOS native later.

**Reasons**:
- Current machine is Windows (no macOS/Xcode available)
- Streamlit provides free hosting and easy deployment
- React/Angular provides modern, responsive UI
- API layer designed for future iOS consumption
- Data models are JSON-compatible and Swift-mappable

**iOS Hooks Ready**:
- RESTful API endpoints for iOS consumption
- JSON data models that map to Swift structs
- Business logic separated from UI
- Auth-ready for future multi-device sync

### Workout Plan Data

The workout plan is a 4-week progressive program:

**Week 1** (10 Min Cardio): Base exercises
- Monday: 25 Pullups, 50 Pushups, 20/3 Bicep Curl, 15/4 Bench Press, 10/4 Shoulder Press
- Tuesday: 25 Squats, 20 Pullups, 15/4 Latpulls, 15/4 Bicep Curl, 15/4 Shoulder Press
- Wednesday: 50 Pushups, 25 Squats, 15/4 Incline Press, 10/4 Chest Flyes, 10/3 Weighted Squats
- Thursday: 20 Pullups, 50 Pushups, 15/4 Bicep Curl, 10/4 Shoulder Press, 15/4 Bench Press
- Friday: 100 Pushups (Close Grip), 40 Squats, 10/3 W Squat, 5/5 Lunges, 10/3 Skull Crusher, 10/3 Tricep
- Saturday: 20 Pullups, 30 Pushups, 15/4 Incline Press, 15/3 Incline Fly, 20/3 Bicep Curl
- Sunday: Rest / Badminton

**Week 2** (10 Min Cardio): Repeats Week 1 with increases
- Monday: +20 Pullups, +55 Pushups
- Tuesday: +40 Squats, +20 Pullups
- Wednesday: +55 Pushups, +40 Squats
- Thursday: +20 Pullups, +55 Pushups
- Friday: +20 Pushups, +60 Squats
- Saturday: +20 Pullups, +30 Pushups
- Sunday: Rest / Badminton

**Week 3** (15 Min Cardio): Repeats Week 2 +1 rep to all exercises
- Sunday: +1 Pullups & Squats, +1 Rep

**Week 4** (15 Min Cardio): Repeats Week 3 +5 reps and +1 set to all exercises
- Sunday: +1 Pullups & Squats, +1 Set

### Exercise Format
- **Bodyweight**: `[reps] [Exercise]` (e.g., "25 Pullups")
- **Weighted**: `[reps]/[sets] [Exercise]` (e.g., "15/4 Bicep Curl" = 15 reps, 4 sets)

### Exercise Library (16 exercises)
| Exercise | Type | Muscle Group |
|----------|------|-------------|
| Pullups | Bodyweight | Back |
| Pushups | Bodyweight | Chest |
| Close Grip Pushup | Bodyweight | Triceps |
| Squats | Bodyweight | Legs |
| Bicep Curl | Weighted | Biceps |
| Bench Press | Weighted | Chest |
| Shoulder Press | Weighted | Shoulders |
| Latpulls | Weighted | Back |
| Incline Press | Weighted | Chest |
| Chest Flyes | Weighted | Chest |
| Weighted Squats | Weighted | Legs |
| W Squat | Weighted | Legs |
| Lunges | Weighted | Legs |
| Skull Crusher | Weighted | Triceps |
| Tricep | Weighted | Triceps |
| Incline Fly | Weighted | Chest |

### Key Files

- `prd.md` - Product Requirements Document with full feature specifications
- `memory.md` - This file, tracking project progress
- `rules.md` - Project rules and guidelines

### Technical Stack (Web-First)

| Component | Technology | Reason |
|-----------|-----------|--------|
| **Frontend** | React (or Angular) | Modern, component-based UI |
| **Backend** | Python FastAPI | Fast development, API-ready |
| **Hosting** | Streamlit | Free hosting, easy deployment |
| **Data Persistence** | Browser localStorage + JSON | Offline-first, simple |
| **Charts** | Chart.js / Recharts | Data visualization |
| **Architecture** | Component-based + API layer | Clean separation, iOS-ready |

### GitHub

- **Repository**: `sameer33337/fitness-tracker` (private)
- **Branch**: `main`
- **Pushed**: 2026-08-17
- **Status**: Code is on GitHub, ready for development

### Next Steps

1. **Set up web app**: Create React/Angular frontend + FastAPI backend + Streamlit hosting
2. **Implement data models**: Exercise, WorkoutPlan, WorkoutWeek, WorkoutExercise, WorkoutLog, CompletedExercise
3. **Load workout plan**: Create workout_plan.json with the 4-week data
4. **Build UI**: Today/Log, Plan, History, Progress, Settings views
5. **Deploy to Streamlit**: Push to GitHub, connect to Streamlit Community Cloud

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### iOS Migration Path (Future)

When macOS/Xcode becomes available:
1. Create SwiftUI app with same data models
2. Consume the FastAPI REST endpoints
3. Add iCloud sync
4. Integrate Apple Health

### Notes

- The app is designed for personal use (Sameer's fitness tracking)
- Web-first approach: React/Angular + Streamlit for immediate deployment
- iOS native hooks ready: API layer, JSON data models, separated business logic
- The 4-week workout plan is the primary data source
- Progressive overload is a key feature (Week 1 → Week 4 progression)
- Two exercise types: bodyweight (reps only) and weighted (reps/sets)