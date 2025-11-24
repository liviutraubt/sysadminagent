import google.adk
import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

ollama_base = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
mcp_url = os.getenv("URL_MCP", "http://localhost:8100/mcp")

#declararea agentului (oblicatoriu root_agent)
root_agent = Agent(
    model=LiteLlm(model="ollama_chat/llama3.2", 
                  api_base=ollama_base), #specificarea modelului cu care interfateaza
    name="SysAdminAgent", #numele agentului
    description="A helpful assistant for administrating Linux-based operating systems.",
     #blocul unde se descrie functionalitatea agentului si modul in care acesta este 
    instruction=r""" 
    You are a system administration assistant.
    
    Only use tools when the user **explicitly requests filesystem operations**.
    
    When asked to perform an action (like greeting or listing files):
    1. Call the appropriate tool.
    2. WAIT for the result.
    3. Use the tool's output to answer the user's question.
    
    Do not invent information. If the tool returns a message, repeat that message to the user as your answer.
    When asked to greet someone, identify the name of that person, 
    call the 'greet' tool with that name, and **print ONLY the tool's returned text as your reply**. 
    Do not summarize, explain, or add extra words — output exactly what the tool returns.
    Example:
    User: Greet LiviuT
    Output: Hello custom function adadad, LiviuT
    When asked to show the contents of a folder, you will most likely be provided with a path. Identify it and pass it to the list_directory tool. You will recieve a list of strings that you will have to print out
    Example: 
    User: Show me the contents of C:\Users\liviu\Documents\UTCN\An 4\Sem I\ASO\Proiect\AgentADK
    Output: The folder provided contains MCP_Server, my_agent
    When asked to show the contents of a file, or to list the content of a given file, you will be provided with the path to that file, that you will pass as an parameter to the get_file_content tool. The tool will return a string that you will print out as a quote. **DO NOT modify the output of the tool. Print it as is **
    Example:
    User: What is the content of C:\Users\liviu\Documents\UTCN\An 4\Sem I\ASO\Proiect\AgentADK\testfile.txt
    Output: File content:"salut bossule"
    """,
    tools=[
        McpToolset(  #conectiunea cu serverul FastMCP prin HTTP (usor de de dockerizat ulterior)
            connection_params=StreamableHTTPConnectionParams(
                url=mcp_url,
            ),
            #tool_filter=["greet", "list_directory"]
        )
    ]
)