import os
import streamlit as st
import random
import time
#import global_ as glob
from dotenv import load_dotenv
from openai import OpenAI
from helper_functions import llm

load_dotenv('helper_functions\.env')
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
llm_model = "gpt-4o"
temp = 0.10

## -- Using LLM to generate --
def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp,
    )
    return response.choices[0].message.content

def get_completion_from_messages(messages, model=llm_model, temperature=temp, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=n
    )
    return response.choices[0].message.content


## -- Initialisation of chat --
def chat_initialisation(selected_approach, lesson_discussion, learning_outcome, num_of_rounds):
    ## Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = llm_model

    # Create session list of responses
    st.session_state.ListOfResp = ListResp()

    ## Display chat messages from history on app rerun
    #for message in st.session_state.messages:
    #    with st.chat_message(message["role"]):
    #        st.markdown(message["content"])

    ## -- Display Discussion Topic through assistant in chat message container --
    if st.session_state.first_prompt == "no":
        with st.chat_message("assistant"):
            stream = get_first_prompt(selected_approach, lesson_discussion, learning_outcome, num_of_rounds)
            #st.write(stream)
        st.session_state.first_prompt = "yes"
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": stream})


## -- Starting prompt for the chat --
def get_first_prompt(selected_approach, lesson_discussion, learning_outcome, num_of_rounds):
    ## -- Generate guiding prompt -- ADR to check what is StartDFR for
    ##llm_prompt = dis.StartDFR(num_of_rounds, selected_approach)
    ## Start of discussion
    prompt = f""" 
    You are an experienced teacher facilitating a discussion among a group of students. 
                    
                    You have opted to use a specific approach to faciliate the discussion. The following text contained in a pair of XML tags describes how this approach works: 
                    <approach>{selected_approach}</approach>
                    
                    You will use the 'Clarify-Sensitise-Influence' process in combination with the aforementioned approach to facilitate the discussion.
                    The following text contained in a pair of XML tags describes what this process involves. 
                    <process>The Clarify-Sensitise-Influence questioning process is used to guide students through a series of questions that foster understanding, awareness, and change in the outlook of the student. These questions guide the facilitation process by scaffolding students’ thinking, and help them to clarify their values and beliefs. Based on the students' responses, teachers guide students to examine their motives behind their decisions or actions, and to take on others-centred perspectives.

1. **Clarify student's thoughts and feelings**:
   - **Objective**: To ensure that students have a clear and shared understanding of the topic, issue, or problem at hand.
   - **Examples of questions to ask**: 'What happened?', 'Who was involved?', 'Why did you do it?', 'How do you feel about it?'
   - **Outcome**: Students should be able to use non-judgemental language to state the facts clearly.

2. **Sensitise them by inviting them to put themselves in the shoes of others**:
   - **Objective**: To raise awareness and empathy among students regarding the nuances and implications of the issue.
   - **Examples of questions to ask**: 'Have you considered the feelings of others?', 'Have you considered the consequences and outcomes of your actions on others?'
   - **Outcome**: Students should be able to express an empathetic response that considered the perspective of other people.

3. **Influence them to make the right decisions**:
   - **Objective**: To guide student towards making informed decisions or adopting new behaviors or attitudes.
   - **Examples of questions to ask**: 'What is the right to do, and why?', 'Do you actions reflect good character, and why?'
   - **Outcome**: Student should be able to express a desire to take action or make decisions that align with the clarified and sensitized understanding of the issue.</process>.

                    This is the scenario of the discussion: <scenario>{lesson_discussion}</scenario>
                    
                    At the end of the discussion, the students should fulfill the following learning outcomes:
                    <learning_outcome>{learning_outcome}</learning_outcome>.
                    
                    You will apply the questioning process over {num_of_rounds} rounds. Use an encouraging and empathetic tone. Remember to consider the chosen approach.
                    Take a deep breath and follow the instructions step-by-step:
                    1. You will generate the first question for the students to answer. This question must be a 'Clarify' question type as described above.
                    2. Do not do anything else until you receive a response from the student. You will wait to receive all responses from all students before responding yourself. 
                    3. Analyse the overall sentiment of all the responses and address the student directly by summarizing their response.
                    4. If any student uses vulgar language, remind the student in the summary that they should try to use appropriate language.
                    5. If any student shows any signs of distress, use an empathetic tone to encourage the student to speak to a trusted adult.
                    6. You will then craft a follow-up question based on the approach and CSI process for the student to answer. State clearly which number question it is and the type of it is in this format 'Question #number# (#Type#):'.
                    7. Repeat steps 2 to 6 until the {num_of_rounds}th question has been given. The {num_of_rounds}th question must be an 'Influence' question type and it must wrap up the discussion.
                    8. After the final set of responses are received, give a brief summary of the entire discussion. Use an encouraging tone and address the students directly.
    """
    st.session_state.mainPrompt = prompt
    
    messages = [{"role": "system", "content": prompt}]
    st.session_state.messages.append({"role": "system", "content": prompt})
    response = get_completion_from_messages(messages)
    #st.session_state.PreviousCollation = response
    return response


## -- Generate student inputs --
def student_resp(num_of_students, lesson_discussion):
    ## Loop through the number of students
    for i in range(num_of_students - 1):
        student_name = f'student{i}'

        # Use the role icon mapping from glob
        icon = glob.role_icons.get(student_name, "❓")  # Default to a question mark if role is not found
        role_display_name = f"{icon} {student_name.capitalize()}"

        ## -- Display student responses in chat message container --
        with st.chat_message(role_display_name):
            stream = random_resp("primary 1", lesson_discussion)
            response = st.write(stream)

        # Add student response to chat history
        st.session_state.messages.append({"role": student_name, "content": response})
        st.session_state.ListOfResp.append(response)
        time.sleep(random.choice(glob.think_time))

## -- Generate random student response --
def random_resp(level, topic):
    random_capability = random.choice(glob.capability)
    lines = random.choice(glob.no_of_lines)
    prompt = f'''Generate an answer with the tone of a {level} student with {random_capability} ability level on the discussion topic <topic>{topic}</topic>. Answer should not be more than {lines} of lines.'''
    #messages = [{"role":"system", "content":prompt}]
    response = llm.get_completion_from_messages(prompt)

    # Select response randomly
    default_response = ["I don't know", "I'm not sure about this topic, can you share more?", response]
    weights = [0.2, 0.1, 0.7]
    selected_response = random.choices(default_response, weights, k=1)[0]
    
    return selected_response

## -- Generate Guiding Prompt -- 1)AsstQuestion = the generated response from llm, 2) PreviousCollation is the main prompt
def get_guide():
    #essageBuilder(st.session_state.ListOfResp, st.session_state.PreviousCollation, st.session_state.messages)
    #st.write(st.session_state.messages)
    next_response = llm.get_completion_from_messages(st.session_state.messages)

    # Clock round
    st.session_state.current_no_of_rounds = st.session_state.current_no_of_rounds + 1
    st.write(f"no of rounds: {st.session_state.current_no_of_rounds}")

    return next_response

## -- Generate an empty list --
def ListResp():
    list_of_Resp = []
    return list_of_Resp

## -- Build message to send to llm -- ADR what is this for?
def MessageBuilder(lsResp, current_response, prev_msg):
    assistant_dict = {"role":"assistant","content":current_response}
    user_dict = {"role":"user","content":str(lsResp)}
    prev_msg.append(assistant_dict)
    prev_msg.append(user_dict)
    return prev_msg


