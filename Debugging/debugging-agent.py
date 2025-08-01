from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import END, START
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")


class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

model=ChatGroq(model = 'llama-3.3-70b-versatile',temperature=0)
def make_default_graph():
    graph_workflow=StateGraph(State)

    def call_model(state):
        return {"messages":[model.invoke(state['messages'])]}
    
    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_edge("agent", END)
    graph_workflow.add_edge(START, "agent")

    agent=graph_workflow.compile()
    return agent

def make_alternative_graph():
    """Make a tool-calling agent"""

    @tool
    def add(a: float, b: float):
        """Adds two numbers."""
        return a + b

    tool_node = ToolNode([add])
    model_with_tools = model.bind_tools([add])
    def call_model(state):
        return {"messages": [model_with_tools.invoke(state["messages"])]}

    def should_continue(state: State):
        if state["messages"][-1].tool_calls:
            return "tools"
        else:
            return END

    graph_workflow = StateGraph(State)

    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_node("tools", tool_node)
    graph_workflow.add_edge("tools", "agent")
    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_conditional_edges("agent", should_continue,{'tools':'tools',END :END})
     

    agent = graph_workflow.compile()
    return agent

agent=make_alternative_graph()





# from typing import Annotated
# from typing_extensions import TypedDict
# from langchain_groq import ChatGroq
# from langgraph.graph import END, START
# from langgraph.graph.state import StateGraph
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode
# from langchain_core.tools import tool
# from langchain_core.messages import BaseMessage
# import os
# from dotenv import load_dotenv

# load_dotenv()
# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
# os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# class State(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

# model = ChatGroq(model='llama-3.3-70b-versatile', temperature=0)

# def make_default_graph():
#     graph_workflow = StateGraph(State)
    
#     def call_model(state):
#         return {"messages": [model.invoke(state['messages'])]}
    
#     graph_workflow.add_node("agent", call_model)
#     graph_workflow.add_edge("agent", END)
#     graph_workflow.add_edge(START, "agent")
#     agent = graph_workflow.compile()
#     return agent

# def make_alternative_graph():
#     """Make a tool-calling agent"""
#     @tool
#     def add(a: float, b: float):
#         """Adds two numbers."""
#         return a + b
    
#     tool_node = ToolNode([add])
#     model_with_tools = model.bind_tools([add])
    
#     def call_model(state):
#         return {"messages": [model_with_tools.invoke(state["messages"])]}
    
#     def should_continue(state: State):
#         last_message = state["messages"][-1]
#         # Check if the last message has tool calls
#         if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
#             return "tools"
#         else:
#             return END
    
#     graph_workflow = StateGraph(State)
#     graph_workflow.add_node("agent", call_model)
#     graph_workflow.add_node("tools", tool_node)
#     graph_workflow.add_edge("tools", "agent")
#     graph_workflow.add_edge(START, "agent")
    
#     # Fixed: Add the conditional edge mapping
#     graph_workflow.add_conditional_edges(
#         "agent", 
#         should_continue,
#         {
#             "tools": "tools",
#             END: END
#         }
#     )
    
#     agent = graph_workflow.compile()
#     return agent

# # Create the agent for LangGraph Studio
# agent = make_alternative_graph()