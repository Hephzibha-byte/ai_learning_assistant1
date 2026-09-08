import os
import json


# --------------------------------
# MEMORY FOLDER AND FILE
# --------------------------------

MEMORY_FOLDER = "memory"

MEMORY_FILE = os.path.join(
    MEMORY_FOLDER,
    "chat_memory.json"
)


# --------------------------------
# CREATE MEMORY FOLDER
# --------------------------------

def initialize_memory():

    os.makedirs(
        MEMORY_FOLDER,
        exist_ok=True
    )


    if not os.path.exists(
        MEMORY_FILE
    ):

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


# --------------------------------
# LOAD MEMORY
# --------------------------------

def load_memory():

    initialize_memory()


    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            messages = json.load(
                file
            )


        return messages


    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


# --------------------------------
# SAVE MEMORY
# --------------------------------

def save_memory(messages):

    initialize_memory()


    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            messages,
            file,
            indent=4,
            ensure_ascii=False
        )


# --------------------------------
# CLEAR MEMORY
# --------------------------------

def clear_memory():

    initialize_memory()


    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [],
            file,
            indent=4
        )