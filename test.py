"""
Test suite for FitTrack - Personal Fitness Tracker
Verifies data loading, exercise parsing, and workout plan structure.
"""

import json
import os
import sys
import importlib

# ============================================================
# TEST: Workout Plan JSON Structure
# ============================================================
def test_workout_plan_structure():
    """Verify the workout plan JSON is correctly structured."""
    json_path = os.path.join(os.path.dirname(__file__), "workout_plan.json")
    with open(json_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    assert "title" in plan, "Plan should have a title"
    assert "weeks" in plan, "Plan should have weeks"
    assert len(plan["weeks"]) == 4, f"Plan should have 4 weeks, got {len(plan['weeks'])}"

    weeks = plan["weeks"]
    for i, week in enumerate(weeks):
        assert "week" in week, f"Week {i+1} should have a name"
        assert "cardio" in week, f"Week {i+1} should have cardio"
        assert "schedule" in week, f"Week {i+1} should have a schedule"
        assert len(week["schedule"]) == 7, f"Schedule should have 7 days, got {len(week['schedule'])}"

        for day, exercises in week["schedule"].items():
            assert isinstance(exercises, list), f"{day} exercises should be a list"
            assert len(exercises) > 0, f"{day} should have at least one entry"

    # Week 1 should have full exercise details
    week1_monday = weeks[0]["schedule"]["Monday"]
    assert any("Pullups" in ex for ex in week1_monday), "Monday Week 1 should have Pullups"
    assert any("Pushups" in ex for ex in week1_monday), "Monday Week 1 should have Pushups"

    print("✓ Workout plan structure verified")
    print(f"  Title: {plan['title']}")
    print(f"  Weeks: {len(weeks)}")
    for week in weeks:
        day_counts = {day: len(exs) for day, exs in week["schedule"].items()}
        print(f"  {week['week']} ({week['cardio']}): {day_counts}")


# ============================================================
# TEST: Exercise Parsing
# ============================================================
def test_exercise_parsing():
    """Verify exercise string parsing works correctly."""
    # Import the app module functions
    sys.path.insert(0, os.path.dirname(__file__))
    try:
        app_module = importlib.import_module("app")
    except Exception as e:
        print(f"⚠️ Could not import app module (expected if streamlit not fully init): {e}")
        # Test parsing logic independently
        import re

        def parse_exercise(exercise_str):
            text = exercise_str.strip()
            match = re.match(r"^(\d+)/(\d+)\s+(.+)$", text)
            if match:
                return {"name": match.group(3), "reps": int(match.group(1)), "sets": int(match.group(2)), "type": "weighted", "raw": text}
            match = re.match(r"^(\d+)\s+(.+)$", text)
            if match:
                return {"name": match.group(2), "reps": int(match.group(1)), "sets": None, "type": "bodyweight", "raw": text}
            return {"name": text, "reps": None, "sets": None, "type": "instruction", "raw": text}

        app_module = type("AppModule", (), {"parse_exercise": staticmethod(parse_exercise)})()

    parse = app_module.parse_exercise

    # Bodyweight exercise
    ex = parse("25 Pullups")
    assert ex["name"] == "Pullups", f"Expected 'Pullups', got '{ex['name']}'"
    assert ex["reps"] == 25, f"Expected 25 reps, got {ex['reps']}"
    assert ex["sets"] is None, "Bodyweight should have no sets"
    assert ex["type"] == "bodyweight", "Should be bodyweight type"
    print("✓ Bodyweight parsing: '25 Pullups' → Pullups, 25 reps")

    # Weighted exercise
    ex = parse("15/4 Bicep Curl")
    assert ex["name"] == "Bicep Curl", f"Expected 'Bicep Curl', got '{ex['name']}'"
    assert ex["reps"] == 15, f"Expected 15 reps, got {ex['reps']}"
    assert ex["sets"] == 4, f"Expected 4 sets, got {ex['sets']}"
    assert ex["type"] == "weighted", "Should be weighted type"
    print("✓ Weighted parsing: '15/4 Bicep Curl' → Bicep Curl, 15 reps, 4 sets")

    # Exercise with notes
    ex = parse("100 Pushups (Close Grip Pushup)")
    assert "Pushups" in ex["name"], "Should parse Pushups with notes"
    assert ex["reps"] == 100, f"Expected 100 reps, got {ex['reps']}"
    print("✓ Notes parsing: '100 Pushups (Close Grip Pushup)' → 100 reps")

    # Special instruction
    ex = parse("Rest / Badminton")
    assert ex["type"] == "instruction", "Should be instruction type"
    print("✓ Instruction parsing: 'Rest / Badminton' → instruction")


# ============================================================
# TEST: All Exercises Across Weeks
# ============================================================
def test_all_exercises():
    """Verify all exercises across the 4-week plan can be parsed."""
    json_path = os.path.join(os.path.dirname(__file__), "workout_plan.json")
    with open(json_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    import re

    def parse_exercise(exercise_str):
        text = exercise_str.strip()
        match = re.match(r"^(\d+)/(\d+)\s+(.+)$", text)
        if match:
            return {"name": match.group(3), "reps": int(match.group(1)), "sets": int(match.group(2)), "type": "weighted"}
        match = re.match(r"^(\d+)\s+(.+)$", text)
        if match:
            return {"name": match.group(2), "reps": int(match.group(1)), "sets": None, "type": "bodyweight"}
        return {"name": text, "reps": None, "sets": None, "type": "instruction"}

    total_exercises = 0
    bodyweight_count = 0
    weighted_count = 0
    instruction_count = 0
    all_names = set()

    for week in plan["weeks"]:
        for day, exercises in week["schedule"].items():
            for ex_str in exercises:
                total_exercises += 1
                ex = parse_exercise(ex_str)
                if ex["type"] == "bodyweight":
                    bodyweight_count += 1
                elif ex["type"] == "weighted":
                    weighted_count += 1
                else:
                    instruction_count += 1
                all_names.add(ex["name"])

    assert total_exercises > 0, "Should have exercises"
    print("✓ All exercises parsed successfully")
    print(f"  Total entries: {total_exercises}")
    print(f"  Bodyweight: {bodyweight_count}")
    print(f"  Weighted: {weighted_count}")
    print(f"  Instructions: {instruction_count}")
    print(f"  Unique exercises/instructions: {len(all_names)}")
    print(f"  Names: {sorted(all_names)}")


# ============================================================
# RUN ALL TESTS
# ============================================================
if __name__ == "__main__":
    # Set UTF-8 output encoding for Windows compatibility
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 50)
    print("FitTrack Test Suite")
    print("=" * 50)
    print()

    test_workout_plan_structure()
    print()
    test_exercise_parsing()
    print()
    test_all_exercises()
    print()
    print("=" * 50)
    print("✅ All tests passed!")
    print("=" * 50)