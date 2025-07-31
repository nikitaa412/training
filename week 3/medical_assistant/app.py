import streamlit as st
import os
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.prompts import PromptTemplate
from tools.all_tools import all_tools
from utils.loader import load_llama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Create uploads folder if not exists
os.makedirs("uploads", exist_ok=True)

# Load LLM model
llm = load_llama()

# Define prompt template for agent
prefix = """You are a helpful medical assistant AI.
You have access to tools for medical document analysis, drug information lookup, symptom checking, and medical condition searches.

Use the following format:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat)
Thought: I now know the final answer
Final Answer: the answer to the original question"""

suffix = """Begin!

Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools=all_tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "agent_scratchpad"],
)

# Create the agent and executor
agent = ZeroShotAgent.from_llm_and_tools(llm=llm, tools=all_tools)  # ✅ Correct
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=all_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=1000,        # Increase as needed
    max_execution_time=None,   # Time in seconds
    early_stopping_method="force"# Prevent infinite loops
)

# Streamlit UI
st.set_page_config(page_title="Medical Assistant", layout="wide")
st.title("🩺 Medical Assistant")

query = st.text_input("Enter your medical question")
uploaded_file = st.file_uploader("Or upload a medical file for analysis (PDF, image, etc.)")

if st.button("Submit"):
    if not query and not uploaded_file:
        st.warning("Please enter a question or upload a file.")
    else:
        with st.spinner("Analyzing..."):
            try:
                if query:
                    # Pass user query text directly
                    response = agent_executor.run(query)
                else:
                    # Save uploaded file and pass file path to agent/tools
                    file_path = os.path.join("uploads", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    # Pass file path as input to the agent
                    response = agent_executor.run(query)
                    print(response)

                st.success("Response:")
                st.markdown(response)
            except Exception as e:
                st.error(f"Agent failed: {e}")
