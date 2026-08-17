"""
FitTrack - ChromaDB Persistence Layer
Handles persistent storage of workout data using ChromaDB.
Saves data when online (for Streamlit Community Cloud deployment).
"""

import json
import hashlib
import random
from datetime import datetime, date
import chromadb


class SimpleEmbeddingFunction:
    """Custom embedding function that doesn't require ONNX model downloads."""

    def name(self):
        return "simple_embedding"

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        embeddings = []
        for text in input:
            hash_val = hashlib.md5(text.encode()).hexdigest()
            embedding = [int(hash_val[i:i+2], 16) / 255.0 for i in range(0, 32, 2)]
            embeddings.append(embedding)
        return embeddings


class WorkoutDatabase:
    """ChromaDB-backed persistence for workout data."""

    def __init__(self, persist_dir="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.logs_collection = self.client.get_or_create_collection(
            name="workout_logs",
            embedding_function=SimpleEmbeddingFunction()
        )
        self.user_collection = self.client.get_or_create_collection(
            name="user_profile",
            embedding_function=SimpleEmbeddingFunction()
        )

    # ========================================
    # WORKOUT LOGS
    # ========================================
    def save_workout_log(self, week_idx, day, exercises, cardio_done, weight_entries=None):
        """Save a workout log to ChromaDB."""
        log_id = f"week{week_idx + 1}_{day.lower()}"
        log_text = json.dumps({
            "week": week_idx,
            "day": day,
            "exercises": exercises,
            "cardio_done": cardio_done,
            "weight_entries": weight_entries or {},
            "date": date.today().isoformat(),
            "timestamp": datetime.now().isoformat(),
        })

        # Upsert the log
        self.logs_collection.upsert(
            ids=[log_id],
            documents=[log_text],
            metadatas=[{
                "week": week_idx,
                "day": day,
                "date": date.today().isoformat(),
                "cardio_done": str(cardio_done).lower(),
                "exercise_count": len(exercises),
            }],
        )
        return True

    def load_all_workout_logs(self):
        """Load all workout logs from ChromaDB."""
        try:
            result = self.logs_collection.get()
            logs = {}
            if result["ids"]:
                for log_id, doc in zip(result["ids"], result["documents"]):
                    log_data = json.loads(doc)
                    key = f"{log_data['week']}|{log_data['day']}"
                    logs[key] = log_data
            return logs
        except Exception:
            return {}

    def has_log(self, week_idx, day):
        """Check if a workout log exists for a week/day."""
        log_id = f"week{week_idx + 1}_{day.lower()}"
        try:
            result = self.logs_collection.get(ids=[log_id])
            return len(result["ids"]) > 0
        except Exception:
            return False

    def delete_all_logs(self):
        """Delete all workout logs from ChromaDB."""
        try:
            result = self.logs_collection.get()
            if result["ids"]:
                self.logs_collection.delete(ids=result["ids"])
            return True
        except Exception:
            return False

    # ========================================
    # USER PROFILE / STATS
    # ========================================
    def save_user_stats(self, stats):
        """Save aggregate user statistics."""
        self.user_collection.upsert(
            ids=["user_stats"],
            documents=[json.dumps(stats)],
            metadatas=[{"updated_at": datetime.now().isoformat()}],
        )
        return True

    def load_user_stats(self):
        """Load aggregate user statistics."""
        try:
            result = self.user_collection.get(ids=["user_stats"])
            if result["ids"]:
                return json.loads(result["documents"][0])
            return {}
        except Exception:
            return {}

    # ========================================
    # AGENTIC RECOMMENDATIONS
    # ========================================
    def generate_recommendations(self, workout_logs, plan):
        """Generate next month's workout recommendations based on captured data.

        Analyzes the user's workout completion patterns and generates
        an agentic recommendation for the next month's training plan.
        """
        if not workout_logs:
            return {
                "summary": "Start logging workouts to get personalized recommendations!",
                "completed_workouts": 0,
                "recommendations": [
                    "Complete Week 1 to establish your baseline"
                ],
                "next_month_plan": "Based on your current progress, complete the existing 4-week plan first."
            }

        # Analyze completion patterns
        completed_workouts = len(workout_logs)
        total_exercises = sum(len(log.get("exercises", [])) for log in workout_logs.values())
        cardio_count = sum(1 for log in workout_logs.values() if log.get("cardio_done"))

        # Analyze which weeks/days are most/least completed
        week_completion = {}
        for key, log in workout_logs.items():
            week_num = log.get("week", 0) + 1
            if week_num not in week_completion:
                week_completion[week_num] = {"days": 0, "exercises": 0}
            week_completion[week_num]["days"] += 1
            week_completion[week_num]["exercises"] += len(log.get("exercises", []))

        # Analyze exercise frequency
        exercise_counts = {}
        for log in workout_logs.values():
            for ex in log.get("exercises", []):
                if ex not in exercise_counts:
                    exercise_counts[ex] = 0
                exercise_counts[ex] += 1

        recommendations = []
        insights = []

        # Generate insights based on patterns
        if completed_workouts > 0:
            insights.append(f"You've completed {completed_workouts} workout(s) with {total_exercises} exercises total.")

        if cardio_count > 0:
            insights.append(f"Cardio completed {cardio_count} time(s).")
        elif completed_workouts > 0:
            insights.append("You haven't logged any cardio sessions yet. Remember to include daily cardio!")

        # Weekly pattern analysis
        if week_completion:
            most_completed_week = max(week_completion.items(), key=lambda x: x[1]["days"])
            insights.append(f"Your most consistent week: Week {most_completed_week[0]} ({most_completed_week[1]['days']} days).")

        # Exercise frequency analysis
        if exercise_counts:
            most_frequent = max(exercise_counts.items(), key=lambda x: x[1])
            insights.append(f"Most frequent exercise: {most_frequent[0]} ({most_frequent[1]} times).")

        # Generate next month recommendations
        covered_days = set()
        for log in workout_logs.values():
            covered_days.add(log.get("day", ""))

        # Recommend based on gaps
        all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        missing_days = [d for d in all_days if d not in covered_days]

        if missing_days:
            recommendations.append(f"Consider adding workouts on: {', '.join(missing_days[:3])}")

        # Determine progression
        if completed_workouts >= 10:
            recommendations.append("Great consistency! Next month, consider increasing weights by 2.5-5kg on compound lifts.")
        elif completed_workouts >= 5:
            recommendations.append("Good progress! Next month, focus on consistency and try to complete all 7 days weekly.")
        else:
            recommendations.append("Build the habit first - aim for at least 5 workout days per week.")

        # Specific exercise recommendations
        if "Bicep Curl" not in exercise_counts and completed_workouts > 0:
            recommendations.append("Add Bicep Curl exercises to balance your arm training.")

        if "Bench Press" not in exercise_counts and completed_workouts > 0:
            recommendations.append("Include Bench Press for strength progression tracking.")

        # Generate next month plan
        next_month_plan = self._build_next_month_plan(week_completion, workout_logs)

        return {
            "summary": f"Based on your {completed_workouts} logged workouts, here's your personalized next month plan.",
            "completed_workouts": completed_workouts,
            "total_exercises": total_exercises,
            "cardio_count": cardio_count,
            "insights": insights,
            "recommendations": recommendations,
            "exercise_frequency": exercise_counts,
            "weekly_completion": week_completion,
            "next_month_plan": next_month_plan,
        }

    def _build_next_month_plan(self, week_completion, workout_logs):
        """Build a next month workout plan based on completion patterns."""
        if not week_completion:
            return "Complete the current 4-week plan first."

        total_days_completed = sum(stats["days"] for stats in week_completion.values())
        if total_days_completed < 7:
            return "Focus on completing all 7 days of the current plan before progressing."

        # Add progressive overload recommendations
        weeks_completed = len(week_completion)
        if weeks_completed >= 4:
            return (
                "Congratulations on completing the 4-week plan! Next month:\n"
                "1. Increase weights by 5-10% on all weighted exercises\n"
                "2. Add +2 reps to all bodyweight exercises\n"
                "3. Increase cardio to 20 minutes\n"
                "4. Add 1-2 new exercises (e.g., Deadlifts, Rows)"
            )
        elif weeks_completed >= 2:
            return (
                "Great progress! For next month:\n"
                "1. Continue the 4-week progressive plan\n"
                "2. Add +5 reps to bodyweight exercises\n"
                "3. Increase cardio duration by 5 minutes\n"
                "4. Track weights for weighted exercises"
            )
        else:
            return (
                "Keep building consistency:\n"
                "1. Complete the current week's exercises\n"
                "2. Aim for 5+ workout days per week\n"
                "3. Track daily cardio\n"
                "4. Rest on Sundays for recovery"
            )


# Singleton instance
_db = None


def get_db():
    """Get the singleton ChromaDB instance."""
    global _db
    if _db is None:
        _db = WorkoutDatabase()
    return _db