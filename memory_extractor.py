import json
from langchain_ollama import ChatOllama

from student_memory import (
    update_student_profile,
    add_important_fact
)


# =========================================================
# MEMORY EXTRACTION MODEL
# =========================================================

memory_llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


# =========================================================
# EXTRACT STUDENT INFORMATION
# =========================================================

def extract_student_memory(user_message):

    prompt = f"""
You are a student memory extraction system.

Read the student's message and identify ONLY useful
long-term information about the student.

Possible information includes:

1. Name
2. Learning goal
3. Preferred subject
4. Important learning preference
5. Other useful long-term learning information

Do NOT save ordinary questions.

Do NOT save temporary information.

Do NOT invent information.

Return ONLY valid JSON.

Use exactly this format:

{{
    "name": "",
    "learning_goal": "",
    "preferred_subject": "",
    "important_fact": ""
}}

If a field is not mentioned, leave it empty.

Student message:

{user_message}
"""


    try:

        response = memory_llm.invoke(
            prompt
        )


        content = response.content.strip()


        # -------------------------------------------------
        # REMOVE MARKDOWN CODE FENCES
        # -------------------------------------------------

        if content.startswith("```"):

            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


        memory_data = json.loads(
            content
        )


        return memory_data


    except Exception as error:

        print(
            f"Memory extraction error: {error}"
        )

        return {
            "name": "",
            "learning_goal": "",
            "preferred_subject": "",
            "important_fact": ""
        }


# =========================================================
# SAVE EXTRACTED MEMORY
# =========================================================

def process_student_message(user_message):

    memory_data = extract_student_memory(
        user_message
    )


    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    if memory_data.get("name"):

        update_student_profile(
            name=memory_data["name"]
        )


    # -----------------------------------------------------
    # LEARNING GOAL
    # -----------------------------------------------------

    if memory_data.get("learning_goal"):

        update_student_profile(
            learning_goal=memory_data[
                "learning_goal"
            ]
        )


    # -----------------------------------------------------
    # PREFERRED SUBJECT
    # -----------------------------------------------------

    if memory_data.get("preferred_subject"):

        update_student_profile(
            preferred_subject=memory_data[
                "preferred_subject"
            ]
        )


    # -----------------------------------------------------
    # IMPORTANT FACT
    # -----------------------------------------------------

    if memory_data.get("important_fact"):

        add_important_fact(
            memory_data["important_fact"]
        )


    return memory_data