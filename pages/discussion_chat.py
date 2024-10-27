import streamlit as st
#from global_ import *
from helper_functions import llm_st as llm

## -- Page Header --
st.title("Discussion Forum (Student)")

## -- Create variables from session state --
num_of_rounds = st.session_state.num_of_rounds
lesson_title = st.session_state.lesson_title
lesson_discussion = st.session_state.lesson_discussion
learning_outcome = st.session_state.learning_outcome
selected_approach_descr = st.session_state.selected_approach_descr
num_of_students = 4
st.session_state.first_prompt = "no"

## -- Display the Discussion Topic --
st.subheader(f":blue[Discussion Topic: {lesson_discussion}]")
st.divider()

## -- Chatbot --
# Initialise
if "initialise" not in st.session_state:
    st.session_state.initialise = "initialised"
    llm.chat_initialisation(selected_approach_descr, lesson_discussion, learning_outcome, num_of_rounds)


## Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] != "system":
            st.markdown(message["content"])

## React to user input
if prompt := st.chat_input("Share your thoughts..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.ListOfResp.append(prompt)

    ## Generate other student responses
    # if num_of_students > 1:
    #     llm.student_resp(num_of_students, lesson_discussion)


## Check if no of rounds completed
# if st.session_state.current_no_of_rounds < num_of_rounds:
    ## Display guiding prompt
    with st.chat_message("assistant"):
        stream = llm.get_guide()
        st.write(stream)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": stream})
# else:
#     ## Display end of lesson
#     with st.chat_message("assistant"):
#         stream = "End of Lesson"
#         response = st.write(stream)

#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})
