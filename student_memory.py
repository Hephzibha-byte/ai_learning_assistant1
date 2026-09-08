import json
import os
from datetime import datetime


# =========================================================
# STUDENT MEMORY CONFIGURATION
# =========================================================

MEMORY_FILE = "student_memory.json"


# =========================================================
# DEFAULT STUDENT MEMORY
# =========================================================

DEFAULT_MEMORY = {
    "student_profile": {
        "name": "",
        "learning_goal": "",
        "preferred_subjects": []
    },

    "learning_progress": {},

    "quiz_performance": [],

    "weak_topics": [],

    "strong_topics": [],

    "important_facts": []
}


# =========================================================
# LOAD STUDENT MEMORY
# =========================================================

def load_student_memory():

    if not os.path.exists(MEMORY_FILE):

        save_student_memory(DEFAULT_MEMORY.copy())

        return DEFAULT_MEMORY.copy()

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            memory = json.load(file)

        return memory

    except Exception:

        return DEFAULT_MEMORY.copy()


# =========================================================
# SAVE STUDENT MEMORY
# =========================================================

def save_student_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4
        )


# =========================================================
# UPDATE STUDENT PROFILE
# =========================================================

def update_student_profile(
    name=None,
    learning_goal=None,
    preferred_subject=None
):

    memory = load_student_memory()

    profile = memory["student_profile"]

    if name:

        profile["name"] = name

    if learning_goal:

        profile["learning_goal"] = learning_goal

    if preferred_subject:

        if preferred_subject not in profile["preferred_subjects"]:

            profile["preferred_subjects"].append(
                preferred_subject
            )

    save_student_memory(memory)

    return memory


# =========================================================
# ADD IMPORTANT FACT
# =========================================================

def add_important_fact(fact):

    if not fact:
        return

    memory = load_student_memory()

    if fact not in memory["important_facts"]:

        memory["important_facts"].append(
            fact
        )

    save_student_memory(memory)


# =========================================================
# ADD QUIZ PERFORMANCE
# =========================================================

def add_quiz_performance(
    topic,
    score,
    total_questions
):

    memory = load_student_memory()

    percentage = (
        score / total_questions
    ) * 100

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    performance = {

        "topic": topic,

        "score": score,

        "total": total_questions,

        "percentage": round(
            percentage,
            1
        ),

        "date": current_time
    }

    memory["quiz_performance"].append(
        performance
    )


    # -----------------------------------------------------
    # UPDATE TOPIC PROGRESS
    # -----------------------------------------------------

    memory["learning_progress"][topic] = {

        "latest_score": round(
            percentage,
            1
        ),

        "last_updated": current_time
    }


    # -----------------------------------------------------
    # UPDATE WEAK / STRONG TOPICS
    # -----------------------------------------------------

    if percentage < 60:

        if topic not in memory["weak_topics"]:

            memory["weak_topics"].append(
                topic
            )

        if topic in memory["strong_topics"]:

            memory["strong_topics"].remove(
                topic
            )


    elif percentage >= 80:

        if topic not in memory["strong_topics"]:

            memory["strong_topics"].append(
                topic
            )

        if topic in memory["weak_topics"]:

            memory["weak_topics"].remove(
                topic
            )


    save_student_memory(memory)

    return performance


# =========================================================
# GET STUDENT MEMORY
# =========================================================

def get_student_memory():

    return load_student_memory()


# =========================================================
# GET MEMORY SUMMARY
# =========================================================

def get_memory_summary():

    memory = load_student_memory()

    profile = memory["student_profile"]

    summary = []


    # -----------------------------------------------------
    # PROFILE
    # -----------------------------------------------------

    if profile["name"]:

        summary.append(
            f"Student name: {profile['name']}"
        )


    if profile["learning_goal"]:

        summary.append(
            f"Learning goal: {profile['learning_goal']}"
        )


    if profile["preferred_subjects"]:

        summary.append(
            "Preferred subjects: "
            + ", ".join(
                profile["preferred_subjects"]
            )
        )


    # -----------------------------------------------------
    # WEAK TOPICS
    # -----------------------------------------------------

    if memory["weak_topics"]:

        summary.append(
            "Weak topics: "
            + ", ".join(
                memory["weak_topics"]
            )
        )


    # -----------------------------------------------------
    # STRONG TOPICS
    # -----------------------------------------------------

    if memory["strong_topics"]:

        summary.append(
            "Strong topics: "
            + ", ".join(
                memory["strong_topics"]
            )
        )


    # -----------------------------------------------------
    # RECENT QUIZ PERFORMANCE
    # -----------------------------------------------------

    recent_quizzes = (
        memory["quiz_performance"][-5:]
    )


    if recent_quizzes:

        summary.append(
            "Recent quiz performance:"
        )


        for quiz in recent_quizzes:

            summary.append(
                f"- {quiz['topic']}: "
                f"{quiz['percentage']}%"
            )


    # -----------------------------------------------------
    # IMPORTANT FACTS
    # -----------------------------------------------------

    if memory["important_facts"]:

        summary.append(
            "Important facts:"
        )


        for fact in memory["important_facts"]:

            summary.append(
                f"- {fact}"
            )


    if not summary:

        return "No student memory available yet."


    return "\n".join(summary)


# =========================================================
# GET PERSONALIZED RECOMMENDATIONS
# =========================================================

def get_personalized_recommendations():

    memory = load_student_memory()

    recommendations = []


    # =====================================================
    # PERFORMANCE-BASED RECOMMENDATIONS
    # =====================================================

    for topic, progress in memory["learning_progress"].items():

        score = progress.get("latest_score")


        if score is None:
            continue


        # -------------------------------------------------
        # CRITICAL: 0–39%
        # -------------------------------------------------

        if score < 40:

            recommendations.append(

                f"🔴 {topic}: Critical improvement needed. "

                f"Your latest score is {score}%. "

                f"Recommended action: revisit the fundamentals, "

                f"study the topic carefully, and practice "
                f"basic questions."

            )


        # -------------------------------------------------
        # WEAK: 40–59%
        # -------------------------------------------------

        elif score < 60:

            recommendations.append(

                f"🟠 {topic}: Focused practice recommended. "

                f"Your latest score is {score}%. "

                f"Recommended action: review core concepts, "

                f"practice important questions, and "
                f"retake the quiz."

            )


        # -------------------------------------------------
        # IMPROVING: 60–79%
        # -------------------------------------------------

        elif score < 80:

            recommendations.append(

                f"🟡 {topic}: You are improving. "

                f"Your latest score is {score}%. "

                f"Recommended action: continue practicing, "

                f"review incorrect answers, and "
                f"attempt another quiz."

            )


        # -------------------------------------------------
        # STRONG: 80–100%
        # -------------------------------------------------

        else:

            recommendations.append(

                f"🟢 {topic}: Strong performance. "

                f"Your latest score is {score}%. "

                f"Recommended action: try advanced questions "

                f"and challenge yourself with harder problems."

            )


    # =====================================================
    # NO QUIZ DATA
    # =====================================================

    if not recommendations:

        recommendations.append(

            "Take a quiz to generate personalized "
            "learning recommendations."

        )


    return recommendations


# =========================================================
# CLEAR STUDENT MEMORY
# =========================================================

def clear_student_memory():

    save_student_memory(
        DEFAULT_MEMORY.copy()
    )
