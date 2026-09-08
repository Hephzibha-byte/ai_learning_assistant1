from langchain_tools import (
    calculator_tool,
    study_plan_tool
)


print("\n--- CALCULATOR TOOL ---")

result = calculator_tool.invoke(
    {
        "expression": "25 * 48"
    }
)

print(result)


print("\n--- STUDY PLAN TOOL ---")

plan = study_plan_tool.invoke(
    {
        "subject": "Python",
        "days": 3,
        "hours_per_day": 2
    }
)

print(plan)