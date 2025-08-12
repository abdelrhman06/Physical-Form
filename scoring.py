"""
Scoring calculation logic for Session Audit Form
Implements complex scoring algorithm based on field values
"""

from typing import Dict, Any

def calculate_break_time_score(break_time_minutes: float) -> int:
    """Calculate break time score based on minutes"""
    if break_time_minutes <= 5:
        return 0
    elif break_time_minutes < 10:
        return 2
    elif break_time_minutes <= 35:
        return 5
    elif break_time_minutes <= 40:
        return 3
    else:
        return 0

def calculate_feedback_score(score: float, thresholds: Dict[int, int]) -> int:
    """Calculate feedback score based on thresholds"""
    for threshold in sorted(thresholds.keys(), reverse=True):
        if score >= threshold:
            return thresholds[threshold]
    return 0

def calculate_session_score(form_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the total session score based on the complex formula
    Returns dict with score, rating, and breakdown
    """
    score = 0
    score_breakdown = {}
    
    # Camera scoring
    camera_score = 0
    if form_data.get("Camera") == "Working":
        camera_score += 5
    score_breakdown["Camera"] = camera_score
    score += camera_score
    
    # Camera quality scoring
    camera_quality_scores = {
        "Clear": 5,
        "Not clear enough": 3,
        "Bad quality": 1,
        "NA": 0
    }
    camera_quality_score = camera_quality_scores.get(form_data.get("Camera quality"), 0)
    score_breakdown["Camera quality"] = camera_quality_score
    score += camera_quality_score
    
    # Camera coverage scoring
    camera_coverage_scores = {
        "Full coverage": 5,
        "Instructor isn't appear": 3,
        "Some students are not appear": 2,
        "Students are not appear": 1,
        "Neither students nor instructor appear": 0
    }
    camera_coverage_score = camera_coverage_scores.get(form_data.get("Camera Coverage"), 0)
    score_breakdown["Camera Coverage"] = camera_coverage_score
    score += camera_coverage_score
    
    # Sound scoring
    sound_scores = {
        "Working excellent": 5,
        "Good quality": 3,
        "Bad quality": 1,
        "Not working": 0
    }
    sound_score = sound_scores.get(form_data.get("Sound"), 0)
    score_breakdown["Sound"] = sound_score
    score += sound_score
    
    # Internet connection scoring
    internet_scores = {
        "Excellent": 5,
        "Frequent Disconnects": 3,
        "Poor Connection": 1,
        "Non-Operational": 0
    }
    internet_score = internet_scores.get(form_data.get("Internet connection"), 0)
    score_breakdown["Internet connection"] = internet_score
    score += internet_score
    
    # Full session scoring
    full_session_score = 10 if form_data.get("Full Session?") == "Yes" else 0
    score_breakdown["Full Session"] = full_session_score
    score += full_session_score
    
    # Students seated scoring
    students_seated_score = 5 if form_data.get("Students seated") == "Yes" else 0
    score_breakdown["Students seated"] = students_seated_score
    score += students_seated_score
    
    # Coordinator appearance scoring
    coordinator_score = 5 if form_data.get("Coordinator appearance") == "Yes" else 0
    score_breakdown["Coordinator appearance"] = coordinator_score
    score += coordinator_score
    
    # Room adequacy scoring
    room_score = 5 if form_data.get("Room adequacy") == "Room adequate" else 0
    score_breakdown["Room adequacy"] = room_score
    score += room_score
    
    # Instructor appearance scoring
    instructor_appearance_score = 5 if form_data.get("Instructor appearance") == "Yes" else 0
    score_breakdown["Instructor appearance"] = instructor_appearance_score
    score += instructor_appearance_score
    
    # Instructor attitude scoring
    instructor_attitude_score = 5 if form_data.get("Instructor Attitude") == "Good" else 0
    score_breakdown["Instructor Attitude"] = instructor_attitude_score
    score += instructor_attitude_score
    
    # English language scoring
    english_scores = {
        "Excellent": 5,
        "Good": 3,
        "Bad": 0,
        "NA": 0
    }
    english_score = english_scores.get(form_data.get("English language of instructor"), 0)
    score_breakdown["English language"] = english_score
    score += english_score
    
    # Slang language scoring (reverse logic)
    slang_score = 5 if form_data.get("Language of instructor (slang language is used)") == "No" else 0
    score_breakdown["Slang language"] = slang_score
    score += slang_score
    
    # Activity scoring
    activity_score = 5 if form_data.get("Activity") == "Yes" else 0
    score_breakdown["Activity"] = activity_score
    score += activity_score
    
    # Break scoring
    break_score = 5 if form_data.get("Break") == "Yes" else 0
    score_breakdown["Break"] = break_score
    score += break_score
    
    # Break time scoring
    break_time = form_data.get("Break Time ( Minutes)", 0)
    break_time_score = calculate_break_time_score(break_time)
    score_breakdown["Break Time"] = break_time_score
    score += break_time_score
    
    # Students feedback scoring
    students_feedback = form_data.get("Students feedback average score", 0)
    students_feedback_thresholds = {95: 10, 90: 8, 85: 6, 80: 4, 75: 2}
    students_feedback_score = calculate_feedback_score(students_feedback, students_feedback_thresholds)
    score_breakdown["Students feedback"] = students_feedback_score
    score += students_feedback_score
    
    # Coordinator feedback scoring
    coordinator_feedback = form_data.get("Coordinator feedback score", 0)
    coordinator_feedback_thresholds = {95: 5, 90: 4, 85: 3, 80: 2, 75: 1}
    coordinator_feedback_score = calculate_feedback_score(coordinator_feedback, coordinator_feedback_thresholds)
    score_breakdown["Coordinator feedback"] = coordinator_feedback_score
    score += coordinator_feedback_score
    
    # Calculate session rating
    if score >= 90:
        rating = "Excellent"
    elif score >= 70:
        rating = "Very Good"
    elif score >= 60:
        rating = "Good"
    else:
        rating = "Bad"
    
    return {
        "total_score": score,
        "session_rating": rating,
        "score_breakdown": score_breakdown,
        "max_possible_score": 100  # Approximate max score for reference
    }

def get_scoring_summary(form_data: Dict[str, Any]) -> str:
    """Generate a human-readable scoring summary"""
    results = calculate_session_score(form_data)
    
    summary = f"""
    **Session Scoring Results**
    
    **Total Score:** {results['total_score']}/100
    **Session Rating:** {results['session_rating']}
    
    **Score Breakdown:**
    """
    
    for category, score in results['score_breakdown'].items():
        summary += f"\n- {category}: {score} points"
    
    return summary
