from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage

from langchain_tools import (
    calculator_tool,
    study_plan_tool
)

from rag_tool import rag_search_tool


# ============================================================
# 1. CREATE QWEN
# ============================================================

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


# ============================================================
# 2. ALL THREE TOOLS
# ============================================================

tools = [
    calculator_tool,
    study_plan_tool,
    rag_search_tool
]


# Create tool lookup dictionary
tool_map = {
    tool.name: tool
    for tool in tools
}


# Give tools to Qwen
llm_with_tools = llm.bind_tools(tools)


# ============================================================
# 3. AGENT FUNCTION
# ============================================================

def run_agent(user_question):

    messages = [
        HumanMessage(content=user_question)
    ]

    # Ask Qwen which tool it needs
    response = llm_with_tools.invoke(messages)

    messages.append(response)

    # ========================================================
    # CHECK FOR TOOL CALLS
    # ========================================================

    if response.tool_calls:

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            print(f"\n🔧 Tool selected: {tool_name}")
            print(f"📥 Tool input: {tool_args}")

            tool = tool_map.get(tool_name)

            if tool is None:

                tool_result = (
                    f"Tool '{tool_name}' was not found."
                )

            else:

                try:

                    tool_result = tool.invoke(
                        tool_args
                    )

                except Exception as e:

                    tool_result = (
                        f"Tool execution failed: {e}"
                    )

            print(f"📤 Tool result:\n{tool_result}")

            # Send result back to Qwen
            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                )
            )

        # ====================================================
        # GET FINAL ANSWER
        # ====================================================

        final_response = llm_with_tools.invoke(
            messages
        )

        return final_response.content

    # ========================================================
    # NO TOOL REQUIRED
    # ========================================================

    return response.content


# ============================================================
# TEST 1 — CALCULATOR
# ============================================================

print("\n========================================")
print("TEST 1 — CALCULATOR")
print("========================================")

answer = run_agent(
    "Calculate 125 * 48"
)

print("\n🤖 FINAL ANSWER:")
print(answer)


# ============================================================
# TEST 2 — STUDY PLAN
# ============================================================

print("\n========================================")
print("TEST 2 — STUDY PLAN")
print("========================================")

answer = run_agent(
    "Create a 5 day study plan for Python with 2 hours per day."
)

print("\n🤖 FINAL ANSWER:")
print(answer)


# ============================================================
# TEST 3 — RAG
# ============================================================

print("\n========================================")
print("TEST 3 — RAG")
print("========================================")

answer = run_agent(
    "According to my uploaded study material, "
    "what is cloud computing?"
)

print("\n🤖 FINAL ANSWER:")
print(answer)