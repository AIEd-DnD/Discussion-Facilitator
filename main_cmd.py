from helper_functions import llm
from DFR_resource import discussion as dis
print("Hello!")
print("Welcome to Discussion Facilitator!")
num_of_students = dis.StudentCounter()
num_of_rounds = dis.RoundCounter()
selected_approach = dis.ApproachSelecter()

#The code below creates the system prompt that will be sent to the LLM to generate the first question and print it out.
llm_prompt=dis.StartDFR(num_of_rounds, selected_approach)
response = llm.get_completion_from_messages(llm_prompt)
print(response)

#The For loop runs for the predetermined number of rounds of discussion: in each round student responses, are collected and processed into the llm_prompt that will be sent again to the LLM.
for i in range(num_of_rounds):
    response = dis.OneRoundOfDiscussion(num_of_students, response, llm_prompt)