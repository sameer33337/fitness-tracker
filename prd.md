# Product Requirements Document (PRD)
## Personal Fitness Tracker - Web App (iOS-Ready)

### 1. Project Overview
**Project Name**: FitTrack - Personal Fitness Tracker
**Target Platform**: Web (React/Angular) hosted on Streamlit, with iOS native hooks ready
**Target Audience**: Personal use - Sameer's fitness tracking
**Core Concept**: A web-based fitness tracker to digitize the 4-week workout plan, allowing easy logging, visualization, and progress tracking of exercises, sets, reps, and weights. Architecture designed to scale to iOS native later.

### 2. Target Platforms
- **Web (Primary)**: React/Angular frontend hosted on Streamlit
- **iOS (Future)**: Native iOS app built with SwiftUI (hooks ready in project)
- **Offline-first**: Data stored locally with cloud sync capability
- **Responsive**: Works on desktop and mobile browsers

### 3. Core Features

#### 3.1 Workout Plan Management
- **Weekly schedule**: Display the 4-week workout plan by day (Monday-Sunday)
- **Daily workout view**: Show exercises for the selected day
- **Progressive overload tracking**: Track weekly progression (Week 1 → Week 2 → Week 3 → Week 4)
- **Cardio tracking**: Log daily cardio sessions (10-15 min)

#### 3.2 Exercise Logging
- **Exercise logging**: Log completed exercises with sets, reps, and weight
- **Two exercise types**:
  - **Bodyweight exercises**: Track reps only (e.g., "25 Pullups", "50 Pushups")
  - **Weighted exercises**: Track reps/sets (e.g., "15/4 Bicep Curl" = 15 reps, 4 sets)
- **Quick add**: Fast entry for logging exercises during workouts
- **Exercise library**: Predefined list of exercises from the workout plan

#### 3.3 Progress Tracking
- **Weekly progress**: Track completion of each week's workout plan
- **Progressive overload**: Visualize how reps/sets increase week over week
- **History view**: Browse past workout sessions by date
- **Personal records (PRs)**: Automatically track personal bests for each exercise

#### 3.4 Data Management
- **Local storage**: Browser localStorage for offline persistence
- **Data export**: Export workout data (CSV/JSON) for backup
- **Data import**: Import workout data from backup
- **API-ready**: Backend API design compatible with future iOS app

#### 3.5 User Interface
- **Tab-based navigation**: Today/Log, Plan, History, Progress, Settings
- **Dark mode support**: Light/dark theme toggle
- **Touch-friendly**: Large tap targets, responsive design
- **Mobile-optimized**: Works on iPhone browsers (320px-375px width)

### 4. Workout Plan Data (Source)

The app is based on the user's 4-week workout plan:

#### Week 1 (10 Min Cardio)
| Day | Exercises |
|-----|-----------|
| **Monday** | 25 Pullups, 50 Pushups, 20/3 Bicep Curl, 15/4 Bench Press, 10/4 Shoulder Press |
| **Tuesday** | 25 Squats, 20 Pullups, 15/4 Latpulls, 15/4 Bicep Curl, 15/4 Shoulder Press |
| **Wednesday** | 50 Pushups, 25 Squats, 15/4 Incline Press, 10/4 Chest Flyes, 10/3 Weighted Squats |
| **Thursday** | 20 Pullups, 50 Pushups, 15/4 Bicep Curl, 10/4 Shoulder Press, 15/4 Bench Press |
| **Friday** | 100 Pushups (Close Grip), 40 Squats, 10/3 W Squat, 5/5 Lunges, 10/3 Skull Crusher, 10/3 Tricep |
| **Saturday** | 20 Pullups, 30 Pushups, 15/4 Incline Press, 15/3 Incline Fly, 20/3 Bicep Curl |
| **Sunday** | Rest / Badminton |

#### Week 2 (10 Min Cardio)
- Repeats Week 1 exercises with increases:
  - Monday: +20 Pullups, +55 Pushups
  - Tuesday: +40 Squats, +20 Pullups
  - Wednesday: +55 Pushups, +40 Squats
  - Thursday: +20 Pullups, +55 Pushups
  - Friday: +20 Pushups, +60 Squats
  - Saturday: +20 Pullups, +30 Pushups
  - Sunday: Rest / Badminton

#### Week 3 (15 Min Cardio)
- Repeats Week 2 and adds **+1 rep** to all exercises
- Sunday: +1 Pullups & Squats, +1 Rep

#### Week 4 (15 Min Cardio)
- Repeats Week 3 and adds **+5 reps and +1 set** to all exercises
- Sunday: +1 Pullups & Squats, +1 Set

#### Exercise Format
- **Bodyweight**: `[reps] [Exercise]` (e.g., "25 Pullups")
- **Weighted**: `[reps]/[sets] [Exercise]` (e.g., "15/4 Bicep Curl" = 15 reps, 4 sets)

#### Exercise Library
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

### 5. Technical Requirements

#### 5.1 Technology Stack (Web-First)
| Component | Technology | Reason |
|-----------|-----------|--------|
| **Frontend** | React (or Angular) | Modern, component-based UI |
| **Backend** | Python FastAPI | Fast development, API-ready |
| **Hosting** | Streamlit | Free hosting, easy deployment |
| **Data Persistence** | Browser localStorage + JSON | Offline-first, simple |
| **Charts** | Chart.js / Recharts | Data visualization |
| **Architecture** | Component-based + API layer | Clean separation, iOS-ready |

#### 5.2 iOS Native Hooks (Future)
The project is designed with iOS native migration in mind:
- **API layer**: RESTful API endpoints that can be consumed by iOS app
- **Data models**: JSON-compatible data structures that map to Swift models
- **Business logic**: Separated from UI for reuse
- **Auth-ready**: API authentication hooks for future multi-device sync

#### 5.3 Data Model (JSON-compatible, Swift-mappable)

##### Exercise
```json
{
  "id": "uuid",
  "name": "Pullups",
  "type": "bodyweight",  // or "weighted"
  "muscleGroup": "back",
  "isCustom": false
}
```

##### WorkoutPlan
```json
{
  "id": "uuid",
  "title": "My Workout Plan",
  "weeks": [WorkoutWeek]
}
```

##### WorkoutWeek
```json
{
  "id": "uuid",
  "weekNumber": 1,
  "cardio": "10 Min Cardio",
  "schedule": {
    "Monday": [WorkoutExercise],
    "Tuesday": [WorkoutExercise]
  }
}
```

##### WorkoutExercise
```json
{
  "id": "uuid",
  "exercise": "Pullups",
  "reps": 25,
  "sets": null,  // null for bodyweight
  "notes": null
}
```

##### WorkoutLog
```json
{
  "id": "uuid",
  "date": "2026-08-17",
  "weekNumber": 1,
  "day": "Monday",
  "completedExercises": [CompletedExercise],
  "cardioCompleted": true
}
```

##### CompletedExercise
```json
{
  "id": "uuid",
  "exercise": "Pullups",
  "plannedReps": 25,
  "plannedSets": null,
  "actualReps": 25,
  "actualSets": null,
  "weight": null,  // in kg for weighted
  "completed": true
}
```

### 6. Non-Functional Requirements

#### 6.1 Performance
- App loads in under 3 seconds
- Smooth 60fps interactions
- Instant data persistence (no noticeable lag)

#### 6.2 Usability
- Log a workout in under 30 seconds
- Intuitive navigation for quick access
- Minimal learning curve
- Mobile-optimized for iPhone browsers

#### 6.3 Reliability
- Offline-first: all features work without internet
- Data never lost (localStorage persistence)
- Graceful error handling

#### 6.4 Security
- Local data only (no cloud storage in MVP)
- Optional biometric lock (future iOS)
- Data export for user-controlled backup

### 7. Future Enhancements (Phase 2)
- **iOS Native App**: SwiftUI app consuming the same API
- iCloud sync across devices
- Apple Health integration
- Workout reminders/notifications
- Rest timer between sets
- Workout templates
- Body measurements tracking
- Calorie tracking
- Social sharing

### 8. Success Metrics
- App launches without errors
- Exercise logging works correctly
- Weekly workout plan displays correctly
- Progressive overload tracking works
- Personal records tracked automatically
- Data persists across browser restarts
- API endpoints ready for iOS consumption

### 9. Development Phases

#### Phase 1: MVP (Web)
- [ ] Project setup (React/Angular + FastAPI + Streamlit)
- [ ] Data models (Exercise, WorkoutPlan, WorkoutLog)
- [ ] Workout plan display (4-week schedule)
- [ ] Exercise logging UI
- [ ] Daily workout view
- [ ] Local data persistence (localStorage)

#### Phase 2: Enhanced Features
- [ ] Progress charts
- [ ] Personal records tracking
- [ ] Progressive overload visualization
- [ ] Dark mode
- [ ] Data export/import
- [ ] API endpoints for iOS readiness

#### Phase 3: iOS Native (Requires macOS)
- [ ] SwiftUI app with same data models
- [ ] API integration with backend
- [ ] iCloud sync
- [ ] Apple Health integration

### 10. Installation & Setup

#### 10.1 Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

#### 10.2 Deployment
1. Push code to GitHub
2. Connect to Streamlit Community Cloud
3. Share the public URL

### 11. File Structure (Planned)

```
Project/fitness-tracker/
├── app.py                     # Streamlit entry point
├── requirements.txt           # Python dependencies
├── frontend/                  # React/Angular frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── services/          # API services
│   │   ├── models/            # Data models
│   │   └── App.jsx            # Main app
│   └── package.json
├── backend/                   # FastAPI backend
│   ├── main.py                # API endpoints
│   ├── models.py              # Data models
│   └── workout_plan.json      # The workout plan data
├── ios/                       # iOS native hooks (future)
│   ├── Models/                # Swift data models
│   └── README.md              # iOS migration guide
├── prd.md                     # This document
├── memory.md                  # Task memory
├── rules.md                   # Project rules
└── README.md                  # Project overview
```

---

## End of PRD