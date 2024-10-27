import streamlit as st
import random
import time
import global_ as glob
from helper_functions import llm


## -- Streamed response emulator --
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


## -- Generate random student response --
def student_resp(level, topic):
    random_capability = random.choice(glob.capability)
    prompt = f'''Generate a response with the tone of a {level} student with {random_capability} ability level on the discussion.'''
    response = llm.get_completion_from_messages(prompt)
    return response