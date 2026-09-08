from langchain_core.tools import tool

from tools import calculate, create_study_plan


# =========================================================
# CALCULATOR TOOL
# =========================================================

@tool
def calculator_tool(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Use this tool when the student asks you to
    perform a mathematical calculation.

    Example:
    25 * 48
    """

    try:
        result = calculate(expression)

        return str(result)

    except Exception as e:

        return f"Could not calculate the expression: {e}"


# =========================================================
# STUDY PLAN TOOL
# =========================================================

@tool
def study_plan_tool(
    subject: str,
    days: int,
    hours_per_day: int
) -> str:
    """
    Create a study plan for a student.

    Use this tool when the student asks for a
    study schedule or study plan.

    subject:
        The subject to study.

    days:
        Number of days available.

    hours_per_day:
        Number of study hours available each day.
    """

    try:

        plan = create_study_plan(
            subject,
            int(days),
            int(hours_per_day)
        )

        return str(plan)

    except Exception as e:

        return f"Could not create study plan: {e}"


# =========================================================
# LIST OF LANGCHAIN TOOLS
# =========================================================

LANGCHAIN_TOOLS = [
    calculator_tool,
    study_plan_tool
]