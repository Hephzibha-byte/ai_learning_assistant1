from agent import run_agent


print("\n===================================")
print("TEST 1 — CALCULATOR")
print("===================================\n")

answer, sources = run_agent(
    "Calculate 125 * 48"
)

print(answer)
print("Sources:", sources)


print("\n===================================")
print("TEST 2 — STUDY PLAN")
print("===================================\n")

answer, sources = run_agent(
    "Create a 5 day Python study plan with 2 hours per day"
)

print(answer)
print("Sources:", sources)


print("\n===================================")
print("TEST 3 — RAG")
print("===================================\n")

answer, sources = run_agent(
    "What is cloud computing?"
)

print(answer)
print("Sources:", sources)
