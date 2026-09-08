from langchain_ollama import ChatOllama
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    SystemMessage
)

from langchain_tools import calculator_tool, study_plan_tool
from rag_tool import rag_search_tool


# ============================================================
# OLLAMA MODEL
# ============================================================

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
)


# ============================================================
# LANGCHAIN TOOLS
# ============================================================

tools = [
    calculator_tool,
    study_plan_tool,
    rag_search_tool
]

tool_map = {
    tool.name: tool
    for tool in tools
}

llm_with_tools = llm.bind_tools(tools)


# ============================================================
# SYSTEM PROMPT
# ============================================================

def build_system_prompt(
    strict_pdf_mode=False,
    conversation_memory="",
    student_memory=""
):

    if strict_pdf_mode:

        mode_instruction = """
STRICT PDF MODE IS ON.

For academic or knowledge questions, you MUST use the
rag_search_tool to search the student's uploaded study material.

Answer ONLY using information returned by the RAG tool.

If the RAG tool does not find relevant information,
say exactly:

I could not find this information in the uploaded study material.

Do NOT use outside knowledge to answer academic questions.

Calculator and study_plan_tool may still be used normally.
"""

    else:

        mode_instruction = """
GENERAL AI MODE IS ON.

For academic questions, FIRST use rag_search_tool to check
the student's uploaded study material.

If the RAG tool returns relevant information, answer using
that material.

If the RAG tool does not contain the answer, you may then
use your general knowledge.

Use calculator_tool for mathematical calculations.

Use study_plan_tool when the student asks for a study schedule
or study plan.
"""

    return f"""
You are an AI Learning Assistant.

Your job is to help a student understand subjects,
study from their uploaded PDFs, perform calculations,
and create study plans.

{mode_instruction}

IMPORTANT TOOL RULES:

1. Mathematical calculation:
   Use calculator_tool.

2. Study schedule / study plan:
   Use study_plan_tool.

3. Questions about uploaded PDFs:
   Use rag_search_tool.

4. Do not invent information from the uploaded PDFs.

5. Give clear, student-friendly answers.

6. When explaining academic concepts, use simple language
   and examples when appropriate.


CONVERSATION MEMORY:

{conversation_memory}


STUDENT MEMORY:

The following information is remembered about the student.

Use this information only when it is relevant to the
student's current request.

Do not invent additional information about the student.

{student_memory}
"""


# ============================================================
# AGENT
# ============================================================

def run_agent(
    user_question: str,
    strict_pdf_mode: bool = False,
    conversation_memory: str = "",
    student_memory: str = ""
):

    # --------------------------------------------------------
    # Build system prompt
    # --------------------------------------------------------

    system_prompt = build_system_prompt(
        strict_pdf_mode=strict_pdf_mode,
        conversation_memory=conversation_memory,
        student_memory=student_memory
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_question)
    ]

    # Keep sources across all tool rounds
    all_sources = []

    # Allow multiple rounds of tool calling
    for _ in range(5):

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        # ----------------------------------------------------
        # No tool needed
        # ----------------------------------------------------

        if not response.tool_calls:
            return response.content, list(set(all_sources))

        # ----------------------------------------------------
        # Execute requested tools
        # ----------------------------------------------------

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            tool = tool_map.get(tool_name)

            # ------------------------------------------------
            # Tool not found
            # ------------------------------------------------

            if tool is None:

                tool_result = (
                    f"Tool '{tool_name}' was not found."
                )

            # ------------------------------------------------
            # Execute tool
            # ------------------------------------------------

            else:

                try:

                    tool_result = tool.invoke(tool_args)

                    # ----------------------------------------
                    # Extract PDF sources
                    # ----------------------------------------

                    if tool_name == "rag_search_tool":

                        result_text = str(tool_result)

                        if "SOURCES:" in result_text:

                            source_section = (
                                result_text.split(
                                    "SOURCES:",
                                    1
                                )[1]
                            )

                            for line in source_section.splitlines():

                                line = line.strip()

                                if line:
                                    all_sources.append(line)

                except Exception as e:

                    tool_result = (
                        f"Tool execution failed: {e}"
                    )

            # ------------------------------------------------
            # Send tool result back to model
            # ------------------------------------------------

            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                )
            )

    # --------------------------------------------------------
    # Maximum tool rounds reached
    # --------------------------------------------------------

    return (
        "I was unable to complete the request.",
        list(set(all_sources))
    )