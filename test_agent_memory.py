from agent import run_agent
from student_memory import get_memory_summary


student_memory = get_memory_summary()

print("\n--- STUDENT MEMORY ---")
print(student_memory)

answer, sources = run_agent(
    user_question="Create a study plan for my exam preparation.",
    strict_pdf_mode=False,
    conversation_memory="",
    student_memory=student_memory
)

print("\n--- AGENT RESPONSE ---")
print(answer)

print("\n--- SOURCES ---")
print(sources)


