import streamlit as st
import sys
import os
from global_ import *
from helper_functions import llm, session
from DFR import approaches_dict as app_dict

## -- Setting up the Headers --
st.title("Case Study Discussion Facilitator")
st.subheader(":blue[Create Lesson (Teacher)]")

## -- Function to pull approaches name (deprecated) --
#def get_variable_names(module):
    #variables = [name for name in dir(module) if not name.startswith("__") and not callable(getattr(module, name))]
    #return variables

#def format_variable_name(name):
    #return name.replace("_", " ").replace("approach", "").strip()


## -- Retreiving all approaches **Norman's update: use dictionary method** --
all_approaches = app_dict.approaches.keys()
#sys.path.append(os.path.join(os.path.dirname(__file__), 'DFR'))
#all_approaches = get_variable_names(approaches)
# Create a mapping from formatted names to original names
#formatted_to_original = {format_variable_name(var): var for var in all_approaches}
#formatted_names = list(formatted_to_original.keys())

## -- Form --
with st.form("createLessonForm", clear_on_submit=True):
    lesson_title = st.text_input("Enter Discussion Topic", "Bullying in School")
    lesson_discussion = st.text_area("Enter Discussion Case Study", "Wei Ling, a 13-year-old secondary school student in Singapore, found herself entangled in the web of bullying during her first year of secondary school. As a newcomer, her quiet demeanor and passion for traditional Chinese calligraphy set her apart from her peers. Unfortunately, Wei Ling's uniqueness became a target for ridicule and scorn, as her classmates viewed her differences with suspicion and hostility. The bullying Wei Ling endured was subtle yet devastating. It started with snide remarks whispered behind her back during group projects and escalated to exclusionary tactics during lunch breaks. She became the subject of hurtful comments and derogatory jokes, both in the physical realm and online. Each insult chipped away at her confidence, leaving her feeling isolated and vulnerable.")
    learning_outcome = st.text_area("Enter Discussion Objectives", "1. Students should understand that bullying can be extremely hurtful.\n2. Students are able to articulate how they can help friends who are faced with bullies.")
    selected_approach = st.selectbox("Select an approach:", all_approaches)
    num_of_rounds = st.slider("Enter no. of Rounds", min_value = 1, max_value = 8)

    # Submission button
    submited = st.form_submit_button("Create Discussion Session")
    if submited:
       # Save actual variable name for approaches dropdown
       #selected_approach = formatted_to_original[selected_formatted_approach]

        # Clear existing chat and session info
       session.clear_session()
       session.clear_chat()

       ## -- Save to session state --
       st.session_state.lesson_title = lesson_title
       st.session_state.lesson_discussion = lesson_discussion
       st.session_state.learning_outcome = learning_outcome
       st.session_state.selected_approach = selected_approach
       st.session_state.selected_approach_descr = app_dict.approaches[selected_approach]
       st.session_state.num_of_rounds = num_of_rounds
       st.session_state.current_no_of_rounds = 0

        # Show successful submission
       st.divider()
       st.write(f'''Lesson created successfully!\n
    Title: {lesson_title}\n
    Discussion Topic: {lesson_discussion}\n
    Learning Outcome: {learning_outcome}\n
    Approach: {selected_approach}\n
    Approach Description: {app_dict.approaches[selected_approach]}\n
    No of Rounds: {num_of_rounds}''')
