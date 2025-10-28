from fastmcp import FastMCP
from os import listdir

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello custom function, {name}"

@mcp.tool
def list_directory(dir_path: str) -> list[str]:
    list = listdir(dir_path)
    return list

@mcp.tool
def get_file_content(file_path: str) -> str:
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8100)