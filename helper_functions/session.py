import streamlit as st

def create_session_states(variables):
    if not st.session_state:
        session_states = {}
        for var in variables:
            session_states[var] = st.session_state.get(var, None)
        return session_states
    else:
        return st.session_state

def update_session_states(session_states, values):
    updated_session_states = {}
    for var, value in values.items():
        session_states[var] = value
        updated_session_states[var] = value
    return updated_session_states

# Function to clear session state
def clear_session():
    st.session_state.clear()

# Function to clear chat messages
def clear_chat():
    st.session_state.messages = []