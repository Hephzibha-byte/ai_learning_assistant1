import os
import json

import streamlit as st
import ollama
from text_to_speech import text_to_speech
from streamlit_mic_recorder import speech_to_text

from langchain_memory import (
    load_chat_history,
    add_user_message,
    add_ai_message
)

from langchain_rag import (
    search_documents,
    add_pdf_to_database
)

from tools import create_study_plan

from memory import (
    load_memory,
    clear_memory
)

from agent import run_agent

from memory_extractor import process_student_message

from student_memory import (
    get_memory_summary,
    add_quiz_performance,
    get_personalized_recommendations
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# LOAD CSS
# =========================================================

def load_css():

    try:

        with open(
            "style.css",
            "r",
            encoding="utf-8"
        ) as file:

            st.markdown(
                f"<style>{file.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        pass


load_css()


# =========================================================
# SESSION STATE
# =========================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = (
        load_chat_history()
    )


if "messages" not in st.session_state:

    st.session_state.messages = (
        load_memory()
    )


if "tool_mode" not in st.session_state:

    st.session_state.tool_mode = None


if "quiz_data" not in st.session_state:

    st.session_state.quiz_data = None


if "quiz_submitted" not in st.session_state:

    st.session_state.quiz_submitted = False


if "quiz_recorded" not in st.session_state:

    st.session_state.quiz_recorded = False


if "quiz_topic" not in st.session_state:

    st.session_state.quiz_topic = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🛠️ Learning Tools")


    # -----------------------------------------------------
    # AI CHAT
    # -----------------------------------------------------

    if st.button(
        "💬 AI Chat",
        use_container_width=True
    ):

        st.session_state.tool_mode = None

        st.rerun()


    # -----------------------------------------------------
    # CLEAR CHAT
    # -----------------------------------------------------

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.chat_history = []

        clear_memory()

        st.session_state.tool_mode = None

        st.rerun()


    # -----------------------------------------------------
    # PDF UPLOAD
    # -----------------------------------------------------

    if st.button(
        "📄 Upload Study PDF",
        use_container_width=True
    ):

        st.session_state.tool_mode = "upload_pdf"

        st.rerun()


    # -----------------------------------------------------
    # STUDY PLAN
    # -----------------------------------------------------

    if st.button(
        "📅 Create Study Plan",
        use_container_width=True
    ):

        st.session_state.tool_mode = "study_plan"

        st.rerun()


    # -----------------------------------------------------
    # QUIZ
    # -----------------------------------------------------

    if st.button(
        "📝 Generate Quiz",
        use_container_width=True
    ):

        st.session_state.tool_mode = "quiz"

        st.session_state.quiz_data = None

        st.session_state.quiz_submitted = False

        st.session_state.quiz_recorded = False

        st.session_state.quiz_topic = ""

        st.rerun()


    # -----------------------------------------------------
    # PROGRESS DASHBOARD
    # -----------------------------------------------------

    if st.button(
        "📊 Progress Dashboard",
        use_container_width=True
    ):

        st.session_state.tool_mode = "dashboard"

        st.rerun()


    st.divider()


    # =====================================================
    # ANSWER MODE
    # =====================================================

    st.subheader("📚 Answer Mode")


    strict_pdf_mode = st.toggle(
        "Strict PDF Mode",
        value=True,
        help=(
            "When enabled, academic answers "
            "use only retrieved study material."
        )
    )


    st.divider()


    # =====================================================
    # RAG STATUS
    # =====================================================

    st.subheader("🧠 RAG Status")


    st.success(
        "Local RAG enabled"
    )


    st.caption(
        "Embedding model: embeddinggemma"
    )


    st.caption(
        "Agent model: qwen3:4b"
    )


    st.caption(
        "Quiz model: gemma3:4b"
    )


    # =====================================================
    # PERSONALIZED LEARNING
    # =====================================================

    st.divider()

    st.subheader("🎯 Personalized Learning")

    recommendations = get_personalized_recommendations()

    if recommendations:

        for recommendation in recommendations:

            st.info(
                recommendation
            )

    else:

        st.caption(
            "Take a quiz to receive personalized recommendations."
        )


# =========================================================
# PAGE TITLE
# =========================================================

st.title(
    "🎓 AI Learning & Study Assistant"
)


st.write(
    "Ask questions from your study materials, "
    "generate interactive quizzes, create study plans "
    "and solve calculations."
)


# =========================================================
# PDF UPLOAD
# =========================================================

if st.session_state.tool_mode == "upload_pdf":

    st.subheader(
        "📄 Upload Your Study Material"
    )


    st.write(
        "Upload a PDF and add it to your "
        "AI Learning Assistant knowledge base."
    )


    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"]
    )


    if uploaded_file is not None:

        st.info(
            f"Selected file: {uploaded_file.name}"
        )


        if st.button(
            "🚀 Add PDF to Knowledge Base",
            type="primary"
        ):

            os.makedirs(
                "documents",
                exist_ok=True
            )


            file_path = os.path.join(
                "documents",
                uploaded_file.name
            )


            # -------------------------------------------------
            # SAVE PDF
            # -------------------------------------------------

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )


            # -------------------------------------------------
            # ADD PDF TO RAG
            # -------------------------------------------------

            try:

                with st.spinner(
                    "Processing PDF and creating embeddings..."
                ):

                    chunks = add_pdf_to_database(
                        file_path
                    )


                st.success(
                    f"🎉 PDF successfully added! "
                    f"{chunks} chunks were added "
                    f"to the knowledge base."
                )


                st.balloons()


            except Exception as error:

                st.error(
                    f"Error processing PDF: {error}"
                )


# =========================================================
# STUDY PLAN
# =========================================================

elif st.session_state.tool_mode == "study_plan":

    st.subheader(
        "📅 Study Plan Generator"
    )


    subject = st.text_input(
        "Enter Subject"
    )


    days = st.number_input(
        "Number of Days",
        min_value=1,
        max_value=30,
        value=7
    )


    hours = st.number_input(
        "Hours Per Day",
        min_value=1,
        max_value=12,
        value=2
    )


    if st.button(
        "Generate Study Plan",
        type="primary"
    ):

        if subject.strip():

            plan = create_study_plan(
                subject,
                int(days),
                int(hours)
            )


            st.success(
                "📚 Your Study Plan"
            )


            st.write(plan)


        else:

            st.warning(
                "Please enter a subject."
            )


# =========================================================
# INTERACTIVE QUIZ
# =========================================================

elif st.session_state.tool_mode == "quiz":

    st.subheader(
        "📝 Interactive Quiz Generator"
    )


    # -----------------------------------------------------
    # QUIZ SETTINGS
    # -----------------------------------------------------

    topic = st.text_input(
        "Enter a topic",
        placeholder="Example: Normalization"
    )


    number_of_questions = st.number_input(
        "Number of Questions",
        min_value=1,
        max_value=10,
        value=5
    )


    # -----------------------------------------------------
    # GENERATE QUIZ
    # -----------------------------------------------------

    if st.button(
        "🚀 Generate Quiz",
        type="primary"
    ):

        if topic.strip():

            context, sources = search_documents(
                topic
            )


            prompt = f"""
You are an AI quiz generator for a student.

Create exactly {number_of_questions}
multiple-choice questions about:

{topic}

Use the following study material:

{context}

IMPORTANT:

Create exactly {number_of_questions} questions.

Each question must have exactly four options.

The correct answer must exactly match
one of the four options.

Keep explanations simple.

Return ONLY valid JSON.

Do not use markdown.

Do not write anything outside the JSON.

Use exactly this format:

[
    {{
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "answer": "Option A",
        "explanation": "Short explanation"
    }}
]
"""


            with st.spinner(
                "Generating your quiz..."
            ):

                try:

                    response = ollama.chat(
                        model="gemma3:4b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )


                    quiz_text = response[
                        "message"
                    ]["content"]


                    quiz_text = quiz_text.strip()


                    # -------------------------------------------------
                    # REMOVE MARKDOWN CODE FENCES
                    # -------------------------------------------------

                    if quiz_text.startswith("```"):

                        quiz_text = (
                            quiz_text
                            .replace("```json", "")
                            .replace("```", "")
                            .strip()
                        )


                    try:

                        quiz_data = json.loads(
                            quiz_text
                        )


                        if not isinstance(
                            quiz_data,
                            list
                        ):

                            raise ValueError(
                                "Quiz is not a list."
                            )


                        if len(quiz_data) != int(
                            number_of_questions
                        ):

                            raise ValueError(
                                "Incorrect number of questions."
                            )


                        # -------------------------------------------------
                        # VALIDATE QUESTIONS
                        # -------------------------------------------------

                        for question in quiz_data:

                            if "question" not in question:

                                raise ValueError(
                                    "Missing question field."
                                )


                            if "options" not in question:

                                raise ValueError(
                                    "Missing options field."
                                )


                            if "answer" not in question:

                                raise ValueError(
                                    "Missing answer field."
                                )


                            if "explanation" not in question:

                                raise ValueError(
                                    "Missing explanation field."
                                )


                            if len(
                                question["options"]
                            ) != 4:

                                raise ValueError(
                                    "Each question must have exactly four options."
                                )


                            if (
                                question["answer"]
                                not in question["options"]
                            ):

                                raise ValueError(
                                    "Correct answer does not match an option."
                                )


                        # -------------------------------------------------
                        # SAVE QUIZ
                        # -------------------------------------------------

                        st.session_state.quiz_data = (
                            quiz_data
                        )


                        st.session_state.quiz_topic = (
                            topic.strip()
                        )


                        st.session_state.quiz_submitted = (
                            False
                        )


                        st.session_state.quiz_recorded = (
                            False
                        )


                        st.success(
                            "🎉 Quiz generated successfully!"
                        )


                        st.rerun()


                    except Exception as error:

                        st.error(
                            "The AI generated an invalid "
                            "quiz format."
                        )


                        st.caption(
                            f"Details: {error}"
                        )


                except Exception as error:

                    st.error(
                        f"Quiz generation error: {error}"
                    )


        else:

            st.warning(
                "Please enter a topic."
            )


    # =====================================================
    # DISPLAY QUIZ
    # =====================================================

    if st.session_state.quiz_data:

        st.divider()


        st.subheader(
            "🎯 Answer the Questions"
        )


        for index, question_data in enumerate(
            st.session_state.quiz_data
        ):

            question_number = index + 1


            st.markdown(
                f"### Question {question_number}"
            )


            st.write(
                question_data["question"]
            )


            st.radio(
                "Choose your answer:",
                question_data["options"],
                key=f"question_{index}"
            )


        st.divider()


        # -------------------------------------------------
        # SUBMIT QUIZ
        # -------------------------------------------------

        if not st.session_state.quiz_submitted:

            if st.button(
                "📤 Submit Quiz",
                type="primary"
            ):

                score = 0


                for index, question_data in enumerate(
                    st.session_state.quiz_data
                ):

                    selected_answer = (
                        st.session_state.get(
                            f"question_{index}"
                        )
                    )


                    correct_answer = (
                        question_data["answer"]
                    )


                    if selected_answer == correct_answer:

                        score += 1


                total_questions = len(
                    st.session_state.quiz_data
                )


                # -------------------------------------------------
                # SAVE PERFORMANCE
                # -------------------------------------------------

                if not st.session_state.quiz_recorded:

                    add_quiz_performance(
                        topic=(
                            st.session_state.quiz_topic
                        ),
                        score=score,
                        total_questions=total_questions
                    )


                    st.session_state.quiz_recorded = (
                        True
                    )


                st.session_state.quiz_submitted = (
                    True
                )


                st.rerun()


        # =================================================
        # RESULTS
        # =================================================

        if st.session_state.quiz_submitted:

            score = 0


            st.subheader(
                "📊 Quiz Results"
            )


            for index, question_data in enumerate(
                st.session_state.quiz_data
            ):

                selected_answer = (
                    st.session_state.get(
                        f"question_{index}"
                    )
                )


                correct_answer = (
                    question_data["answer"]
                )


                if selected_answer == correct_answer:

                    score += 1


            total_questions = len(
                st.session_state.quiz_data
            )


            percentage = (
                score / total_questions
            ) * 100


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Your Score",
                    f"{score} / {total_questions}"
                )


            with col2:

                st.metric(
                    "Percentage",
                    f"{percentage:.1f}%"
                )


            st.progress(
                int(percentage)
            )


            # -------------------------------------------------
            # ANSWER REVIEW
            # -------------------------------------------------

            st.divider()


            st.subheader(
                "📖 Answer Review"
            )


            for index, question_data in enumerate(
                st.session_state.quiz_data
            ):

                selected_answer = (
                    st.session_state.get(
                        f"question_{index}"
                    )
                )


                correct_answer = (
                    question_data["answer"]
                )


                st.markdown(
                    f"### Question {index + 1}"
                )


                st.write(
                    question_data["question"]
                )


                if selected_answer:

                    st.write(
                        f"Your answer: {selected_answer}"
                    )

                else:

                    st.write(
                        "Your answer: Not answered"
                    )


                if selected_answer == correct_answer:

                    st.success(
                        f"✅ Correct! "
                        f"Answer: {correct_answer}"
                    )

                else:

                    st.error(
                        f"❌ Correct answer: "
                        f"{correct_answer}"
                    )


                st.info(
                    question_data["explanation"]
                )


            # -------------------------------------------------
            # PERFORMANCE MESSAGE
            # -------------------------------------------------

            if percentage >= 80:

                st.success(
                    "🎉 Excellent work! "
                    "You understand this topic very well."
                )


            elif percentage >= 50:

                st.warning(
                    "👍 Good attempt! "
                    "Review the incorrect answers."
                )


            else:

                st.error(
                    "📚 You should review this topic "
                    "and try the quiz again."
                )


            # -------------------------------------------------
            # PERSONALIZED RECOMMENDATION
            # -------------------------------------------------

            st.divider()

            st.subheader(
                "🎯 Your Personalized Recommendation"
            )

            current_recommendations = (
                get_personalized_recommendations()
            )

            for recommendation in current_recommendations:

                st.info(
                    recommendation
                )


            # -------------------------------------------------
            # CLEAR QUIZ
            # -------------------------------------------------

            if st.button(
                "🔄 Clear Quiz"
            ):

                st.session_state.quiz_data = None

                st.session_state.quiz_submitted = (
                    False
                )

                st.session_state.quiz_recorded = (
                    False
                )

                st.session_state.quiz_topic = ""

                st.rerun()


elif st.session_state.tool_mode == "dashboard":

    st.subheader("📊 Student Progress Dashboard")

    st.write(
        "Track your quiz performance, strong topics, "
        "weak topics and personalized recommendations."
    )

    try:

        with open(
            "student_memory.json",
            "r",
            encoding="utf-8"
        ) as file:

            student_data = json.load(file)

    except Exception:

        student_data = {
            "learning_progress": {},
            "quiz_performance": [],
            "weak_topics": [],
            "strong_topics": []
        }

    quiz_performance = student_data.get(
        "quiz_performance", []
    )

    learning_progress = student_data.get(
        "learning_progress", {}
    )

    weak_topics = student_data.get(
        "weak_topics", []
    )

    strong_topics = student_data.get(
        "strong_topics", []
    )

    total_quizzes = len(quiz_performance)
    total_topics = len(learning_progress)

    if total_quizzes > 0:

        percentages = [
            float(quiz.get("percentage", 0))
            for quiz in quiz_performance
        ]

        average_score = sum(percentages) / total_quizzes
        best_score = max(percentages)

    else:

        average_score = 0
        best_score = 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📝 Quizzes Taken", total_quizzes)

    with col2:
        st.metric("📊 Average Score", f"{average_score:.1f}%")

    with col3:
        st.metric("🏆 Best Score", f"{best_score:.1f}%")

    with col4:
        st.metric("📚 Topics Studied", total_topics)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🟢 Strong Topics")

        if strong_topics:
            for topic in strong_topics:
                st.success(f"✓ {topic}")
        else:
            st.info("No strong topics yet. Keep practicing!")

    with col2:

        st.subheader("🔴 Topics to Improve")

        if weak_topics:
            for topic in weak_topics:
                st.error(f"• {topic}")
        else:
            st.info("No weak topics identified yet.")

    st.divider()

    st.subheader("📈 Quiz History")

    if quiz_performance:

        for quiz in reversed(quiz_performance):

            percentage = float(quiz.get("percentage", 0))
            topic = quiz.get("topic", "Unknown")
            score = quiz.get("score", 0)
            total = quiz.get("total", 0)
            date = quiz.get("date", "")

            st.write(
                f"**{topic}** — {score}/{total} "
                f"({percentage:.1f}%)"
            )

            st.progress(min(100, max(0, int(percentage))))

            if date:
                st.caption(f"📅 {date}")

    else:
        st.info("Take a quiz to see your progress here.")

    st.divider()

    st.subheader("🎯 Personalized Recommendations")

    recommendations = get_personalized_recommendations()

    if recommendations:
        for recommendation in recommendations:
            st.info(recommendation)
    else:
        st.info(
            "Complete a quiz to receive personalized recommendations."
        )



# =========================================================
# AI CHAT — LANGCHAIN AGENT
# =========================================================

else:

    st.subheader(
        "💬 AI Study Chat"
    )


    # -----------------------------------------------------
    # DISPLAY CHAT HISTORY
    # -----------------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # -----------------------------------------------------
    # USER INPUT
    # -----------------------------------------------------

    # =========================================================
    # TEXT + VOICE INPUT
    # =========================================================

    col1, col2 = st.columns([6, 1])

    with col1:

        typed_question = st.chat_input(
            "Ask something about Python, DBMS or Cloud Computing..."
        )

    with col2:

        voice_question = speech_to_text(
            language="en",
            start_prompt="🎤",
            stop_prompt="⏹️",
            just_once=True
        )

    if voice_question:

        user_question = voice_question

    else:

        user_question = typed_question


    if user_question:

        # =================================================
        # SAVE USER MESSAGE
        # =================================================

        user_message = {
            "role": "user",
            "content": user_question
        }

        st.session_state.messages.append(
            user_message
        )

        add_user_message(
            st.session_state.chat_history,
            user_question
        )

        # =================================================
        # STUDENT MEMORY EXTRACTION
        # =================================================

        try:

            process_student_message(
                user_question
            )

        except Exception as error:

            print(
                f"Student memory error: {error}"
            )

        with st.chat_message("user"):

            st.markdown(
                user_question
            )

        # =================================================
        # CONVERSATION MEMORY
        # =================================================

        recent_history = (
            st.session_state.chat_history[-10:]
        )

        conversation_memory = "\n".join(
            [
                f"{message.type}: {message.content}"
                for message in recent_history
            ]
        )

        # =================================================
        # STUDENT MEMORY
        # =================================================

        student_memory = get_memory_summary()

        recommendations = (
            get_personalized_recommendations()
        )

        recommendation_text = "\n".join(
            f"- {recommendation}"
            for recommendation in recommendations
        )

        student_memory = (
            student_memory
            + "\n\nPersonalized recommendations:\n"
            + recommendation_text
        )

        # =================================================
        # LANGCHAIN AGENT
        # =================================================

        with st.chat_message("assistant"):

            with st.spinner("🧠 Thinking..."):

                try:

                    answer, sources = run_agent(
                        user_question=user_question,
                        strict_pdf_mode=strict_pdf_mode,
                        conversation_memory=conversation_memory,
                        student_memory=student_memory
                    )

                except Exception as error:

                    answer = (
                        "Sorry, I encountered an error "
                        "while processing your question."
                    )

                    sources = []

                    st.error(
                        f"Agent error: {error}"
                    )

            st.markdown(answer)

            # =================================================
            # PHASE 10.6 — TEXT TO SPEECH
            # =================================================

            if st.button(
                "🔊 Read Aloud",
                key=f"read_aloud_{len(st.session_state.messages)}",
                use_container_width=True
            ):

                with st.spinner("🔊 Generating audio..."):

                    audio_file = text_to_speech(answer)

                if audio_file:

                    st.success("🔊 Audio generated!")

                    st.audio(
                        audio_file,
                        format="audio/mp3",
                        autoplay=True
                    )

                else:

                    st.error(
                        "❌ Could not generate audio. "
                        "Check your internet connection."
                    )

            # -------------------------------------------------
            # SOURCES
            # -------------------------------------------------

            if sources:

                st.caption(
                    "📚 Sources: "
                    + ", ".join(sources)
                )


        # =================================================
        # SAVE AI ANSWER
        # =================================================

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


        add_ai_message(
            st.session_state.chat_history,
            answer
        )



