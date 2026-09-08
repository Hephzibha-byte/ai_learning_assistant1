import ast
import operator


# --------------------------------
# STUDY PLAN TOOL
# --------------------------------

def create_study_plan(subject, days, hours_per_day):

    subject = subject.strip()

    # Topic breakdown for common subjects
    topic_map = {

        "python": [
            "Python Basics",
            "Control Flow",
            "Functions and Modules",
            "Data Structures",
            "Object-Oriented Programming",
            "File Handling and Exceptions",
            "Mini Project and Revision"
        ],

        "dbms": [
            "DBMS Basics and Architecture",
            "ER Model and Relational Model",
            "SQL Queries",
            "Normalization",
            "Transactions and Concurrency",
            "Indexing and Database Design",
            "Revision and Practice"
        ],

        "cloud computing": [
            "Cloud Computing Basics",
            "Cloud Service Models",
            "Cloud Deployment Models",
            "Virtualization",
            "Cloud Security",
            "Cloud Storage and Networking",
            "Revision and Real-World Examples"
        ],

        "computer networks": [
            "Networking Basics",
            "OSI and TCP/IP Models",
            "Data Link Layer",
            "Network Layer",
            "Transport Layer",
            "Application Layer",
            "Revision and Practice"
        ],

        "javascript": [
            "JavaScript Basics",
            "Variables and Data Types",
            "Functions and Callbacks",
            "Arrays and Objects",
            "DOM Manipulation",
            "Events and Asynchronous JavaScript",
            "Mini Project and Revision"
        ],

        "html": [
            "HTML Basics",
            "Text and Links",
            "Images and Multimedia",
            "Tables and Forms",
            "Semantic HTML",
            "HTML5 Features",
            "Practice Project"
        ],

        "css": [
            "CSS Basics",
            "Selectors and Properties",
            "Box Model",
            "Flexbox",
            "Grid",
            "Responsive Design",
            "Practice Project"
        ]
    }

    subject_key = subject.lower()

    # Use predefined topics if available
    if subject_key in topic_map:
        topics = topic_map[subject_key]

    else:
        # Generic plan for any subject
        topics = [
            f"{subject} Basics",
            f"Core Concepts of {subject}",
            f"Important Topics in {subject}",
            f"Advanced Concepts of {subject}",
            f"Practical Applications of {subject}",
            f"Practice and Problem Solving",
            f"Revision and Mock Test"
        ]

    plan = []

    # Distribute topics across available days
    for day in range(1, days + 1):

        topic_index = (day - 1) % len(topics)
        topic = topics[topic_index]

        # Divide study time into smaller sessions
        concept_time = max(30, int(hours_per_day * 60 * 0.4))
        practice_time = max(20, int(hours_per_day * 60 * 0.35))
        revision_time = max(10, int(hours_per_day * 60 * 0.25))

        plan.append(
            f"Day {day} — {topic}\n"
            f"  • Learn concepts: {concept_time} minutes\n"
            f"  • Practice: {practice_time} minutes\n"
            f"  • Revision: {revision_time} minutes"
        )

    return "\n\n".join(plan)


# --------------------------------
# SAFE CALCULATOR TOOL
# --------------------------------

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def calculate(expression):

    try:

        node = ast.parse(
            expression,
            mode="eval"
        ).body

        result = evaluate(node)

        return str(result)

    except Exception:

        return "Invalid mathematical expression."


def evaluate(node):

    if isinstance(node, ast.Constant):

        return node.value

    if isinstance(node, ast.BinOp):

        left = evaluate(node.left)

        right = evaluate(node.right)

        operation = operators[type(node.op)]

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):

        value = evaluate(node.operand)

        operation = operators[type(node.op)]

        return operation(value)

    raise ValueError("Invalid expression")