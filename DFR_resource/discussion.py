from helper_functions import llm

def StartDFR(num_of_rounds, approach):
    scenario = input("Please describe the issue or scenario that you would like your students to discuss: ")
    print(" ")
    learning_outcome = input("Please state what you would like your students to achieve by the end of this discussion: ")
    print(" ")
    system_message = f""" 
                    You are an experienced teacher facilitating a discussion among a group of students. 
                    
                    You have opted to use a specific approach to faciliate the discussion. The following text contained in a pair of XML tags describes how this approach works: 
                    <approach>{approach}</approach>
                    
                    You will use the 'Clarify-Sensitise-Influence' process in combination with the aforementioned approach to facilitate the discussion.
                    The following text contained in a pair of XML tags describes what this process involves. 
                    <process>The Clarify-Sensitise-Influence questioning process is used to guide students through a series of questions that foster understanding, awareness, and change in the outlook of the student. These questions guide the facilitation process by scaffolding students’ thinking, and help them to clarify their values and beliefs. Based on the students' responses, teachers guide students to examine their motives behind their decisions or actions, and to take on others-centred perspectives.

1. **Clarify students' thoughts and feelings**:
   - **Objective**: To ensure that students have a clear and shared understanding of the topic, issue, or problem at hand.
   - **Examples of questions to ask**: 'What happened?', 'Who was involved?', 'Why did you do it?', 'How do you feel about it?'
   - **Outcome**: Students should be able to use non-judgemental language to state the facts clearly.

2. **Sensitise them by inviting them to put themselves in the shoes of others**:
   - **Objective**: To raise awareness and empathy among students regarding the nuances and implications of the issue.
   - **Examples of questions to ask**: 'Have you considered the feelings of others?', 'Have you considered the consequences and outcomes of your actions on others?'
   - **Outcome**: Students should be able to express an empathetic response that considered the perspective of other people.

3. **Influence them to make the right decisions**:
   - **Objective**: To guide students towards making informed decisions or adopting new behaviors or attitudes.
   - **Examples of questions to ask**: 'What is the right to do, and why?', 'Do you actions reflect good character, and why?'
   - **Outcome**: Students should be able to express a desire to take action or make decisions that align with the clarified and sensitized understanding of the issue.</process>.

                    This is the scenario of the discussion: <scenario>{scenario}</scenario>
                    
                    At the end of the discussion, the students should fulfill the following learning outcomes:
                    <learning_outcome>{learning_outcome}</learning_outcome>.
                    
                    You will apply the questioning process over {num_of_rounds} rounds. Use an encouraging and empathetic tone. Remember to consider the chosen approach.
                    Take a deep breath and follow the instructions step-by-step:
                    1. You will generate the first question for the students to answer. This question must be a 'Clarify' question type as described above.
                    2. Do not do anything else until you receive a response from the students. You will wait to receive a python list of responses: each response in that list comes from one participating student. You are to restate word-for-word the exact response of each student as part of your reply.
                    3. Analyse the overall sentiment of all the responses and address the students directly by summarizing their responses.
                    4. If any student uses vulgar language, remind the students in the summary that they should try to use appropriate language.
                    5. If any student shows any signs of distress, use an empathetic tone to encourage the student to speak to a trusted adult.
                    6. You will then craft a follow-up question based on the approach and CSI process for the students to answer. State clearly which number question it is and the type of it is in this format 'Question #number# (#Type#):'.
                    7. Repeat steps 2 to 6 until the {num_of_rounds}th question has been given. The {num_of_rounds}th question must be an 'Influence' question type and it must wrap up the discussion.
                    8. After the final set of responses are received, give a brief summary of the discussion. Use an encouraging tone and address the students directly.

                    """
    messages = [{"role":"system", "content":system_message}]
    return messages

def firstAsstMsg(lsResp, msg):
    asst_dict = {"role":"assistant","content":msg}
    lsResp.append(asst_dict)
    return lsResp


def StudResp():
    """
    Calling this function allows the system to take in a student response as input.
    """
    resp = input("Type in your response to the question: ")
    return resp

def ListResp():
    """
    Calling this function generates and empty list, which will be used to store all student responses.
    """
    list_of_Resp = []
    return list_of_Resp

def CollateResp(lsResp, Resp):
    """
    Calling this function with a list and a student response will append a student's response to that list.
    """
    lsResp.append(Resp)
    return lsResp

def MessageBuilder(lsResp, current_response, prev_msg):
    """
    Calling this function will help to build the message to be sent to ChatGPT.
    """
    assistant_dict = {"role":"assistant","content":current_response}
    user_dict = {"role":"user","content":str(lsResp)}
    prev_msg.append(assistant_dict)
    prev_msg.append(user_dict)
    return prev_msg

def OneRoundOfDiscussion(num_of_students, AsstQuestion, PreviousCollation):
    ListOfResp = ListResp()
    for i in range(num_of_students):
        student_resp = StudResp()
        CollateResp(ListOfResp, student_resp)
    MessageBuilder(ListOfResp, AsstQuestion, PreviousCollation)
    next_response = llm.get_completion_from_messages(PreviousCollation)
    print(next_response)
    return next_response

def RoundCounter():
    number = input("How many rounds of dialogue should this discussion have? ")
    return int(number)

def StudentCounter():
    number = input("How many students are in this discussion group? ")
    return int(number)

def ApproachSelecter():
    print("You may opt for the following faciliation approaches:")
    approach_menu = """
    1. Narrative Approach
    2. Experiential Approach
    3. Consideration Approach
    4. Cognitive Development Approach
    5. Modified Values Approach
    """
    print(approach_menu)
    approach_selection = input("Please select the approach you would like by entering the number: ")

    if approach_selection == "1":
        selected_approach = narrative_approach
    elif approach_selection == "2":
        selected_approach = exp_approach
    elif approach_selection == "3":
        selected_approach = consideration_approach
    elif approach_selection == "4":
        selected_approach = cognitive_dev_approach
    elif approach_selection == "5":
        selected_approach = modified_values_approach
    
    return selected_approach

#Everything below this line contains description of the approaches. Do not enter any additional functionality below this line.
narrative_approach = """
Students are guided to identify and clarify their personal
beliefs and values when they relate their personal experiences,
construct their own stories or consider the experiences of
others. Teachers use the questioning process to help students
take perspectives, clarify their feelings and reflect on how
they can apply their learning to their daily lives. Through this,
students understand the need to practise good values, and 
learn how they are expressed through concrete actions.
"""
exp_approach = """
Students go through a cycle of experiences, observation,
reflection and application in real-world situations or scenarios
to help them internalise the values. Teachers facilitate
dialogue and sharing of personal experiences to help students
reflect on the values, skills and attitudes learnt, and suggest
how they can be applied in their daily lives.
"""
consideration_approach = """
Through effective questioning, teachers help students
examine at issues from different perspectives. By considering
the impact of one's decisions on others, they learn to be more
sensitive to the feelings of others. This helps to develop in
them the capacity for empathy, and an ability to make sound
decisions based on a balanced understanding of any situation.
"""
cognitive_dev_approach = """
Students are brought through the process of moral
reasoning to help them examine the motives behind their
actions, and consider common good when deciding on the
right thing to do. Teachers use the questioning process to
help students progress from a self-centred perspective to
a higher level of moral reasoning focusing on societal and
universal perspectives using Kohlberg's six stages of moral
development.
"""
modified_values_approach = """
Teachers use the questioning process to guide students
to clarify their beliefs and values through examining their
personal feelings, Uuderstanding the values and beliefs held
by others and considering the impact of their actions on others.
In this way, students are better able to make informed and
responsible decisions based on a sound value system.
"""