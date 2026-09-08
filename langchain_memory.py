from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from memory import (
    load_memory,
    save_memory
)


# --------------------------------
# LOAD LANGCHAIN CHAT HISTORY
# --------------------------------

def load_chat_history():

    saved_messages = load_memory()

    chat_history = []


    for message in saved_messages:

        role = message.get(
            "role",
            ""
        )

        content = message.get(
            "content",
            ""
        )


        if role == "user":

            chat_history.append(
                HumanMessage(
                    content=content
                )
            )


        elif role == "assistant":

            chat_history.append(
                AIMessage(
                    content=content
                )
            )


    return chat_history


# --------------------------------
# SAVE LANGCHAIN CHAT HISTORY
# --------------------------------

def save_chat_history(
    chat_history
):

    messages_to_save = []


    for message in chat_history:

        if isinstance(
            message,
            HumanMessage
        ):

            role = "user"


        elif isinstance(
            message,
            AIMessage
        ):

            role = "assistant"


        else:

            continue


        messages_to_save.append(
            {
                "role": role,
                "content": message.content
            }
        )


    save_memory(
        messages_to_save
    )


# --------------------------------
# ADD USER MESSAGE
# --------------------------------

def add_user_message(
    chat_history,
    content
):

    chat_history.append(
        HumanMessage(
            content=content
        )
    )


    save_chat_history(
        chat_history
    )


# --------------------------------
# ADD AI MESSAGE
# --------------------------------

def add_ai_message(
    chat_history,
    content
):

    chat_history.append(
        AIMessage(
            content=content
        )
    )


    save_chat_history(
        chat_history
    )