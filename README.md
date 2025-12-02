# System Administration AI Agent

A containerized AI agent system built with Google ADK, FastMCP, and Ollama for Linux system administration tasks. The agent can interact with the filesystem through Model Context Protocol (MCP) tools.

## Architecture

This project consists of three main components running in Docker containers:

1. **Ollama Server**: Runs the Llama 3.2 language model
2. **MCP Server**: Provides filesystem operation tools via FastMCP
3. **ADK Agent**: Google ADK-based agent that orchestrates tool usage

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Ollama    │◄────────│  ADK Agent  │────────►│ MCP Server  │
│  (LLM)      │         │  (Google)   │         │  (Tools)    │
└─────────────┘         └─────────────┘         └─────────────┘
     :11434                 :8000                    :8100
```

## Features

The agent provides the following capabilities through MCP tools:

- **Greet**: Custom greeting function
- **List Directory**: Browse directory contents
- **Get File Content**: Read and display file contents

## Prerequisites

- Docker and Docker Compose
- Network: `aso_network` (external network must be created first)

## Setup

1. **Create the external network**:
   ```bash
   docker network create aso_network
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

3. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

4. **Wait for services to initialize**:
   The Ollama container will automatically pull and run the Llama 3.2 model on first startup. This may take several minutes.

## Usage

Once all containers are running, access the agent web interface at:
```
http://localhost:8000
```

### Example Commands

**Greeting**:
```
Greet John
```
Expected output: `Hello custom function, John`

**List Directory**:
```
Show me the contents of /usr/src/app
```
Expected output: List of files and folders in the specified directory

**Read File**:
```
What is the content of /path/to/file.txt
```
Expected output: `File content: "<file contents>"`

## Project Structure

```
.
├── docker-compose.yml          # Main orchestration file
├── requirements.txt            # Python dependencies (reference)
├── .gitignore                  # Git ignore rules
│
├── MCP_Server/                 # FastMCP server component
│   ├── Dockerfile
│   ├── requirements.txt
│   └── my_server.py           # MCP tool definitions
│
├── docker-agent-deploy/        # Google ADK agent component
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── my_agent/
│       ├── __init__.py
│       └── agent.py           # Agent configuration
│
└── ollama/                     # Ollama LLM service
    └── Dockerfile
```

## Configuration

### Environment Variables

The following environment variables are configured in `docker-compose.yml`:

- `OLLAMA_API_BASE`: Ollama API endpoint (default: `http://ollama:11434`)
- `URL_MCP`: MCP server endpoint (default: `http://mcp_server:8100/mcp`)

### Ports

- **8000**: ADK Agent web interface (mapped from container port 8000)
- **8100**: MCP Server API (mapped to host port 8101)
- **11434**: Ollama API (mapped to host port 11435)

## Adding New Tools

To add new MCP tools, edit `MCP_Server/my_server.py`:

```python
@mcp.tool
def your_new_tool(param: str) -> str:
    # Your implementation
    return result
```

Then update the agent instructions in `docker-agent-deploy/my_agent/agent.py` to teach the agent how to use the new tool.

## Troubleshooting

### Container Startup Issues

Check container logs:
```bash
docker-compose logs -f [service_name]
```

Services: `ollama`, `mcp_server`, `adk_agent`

### Network Connection Issues

Ensure the external network exists:
```bash
docker network ls | grep aso_network
```

If not found, create it:
```bash
docker network create aso_network
```

### Ollama Model Not Loading

The Ollama container pulls the model on first run. Check logs:
```bash
docker-compose logs ollama
```

Wait for the message indicating the model is ready.

## Development

### Local Development Without Docker

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run components individually (ensure Ollama is running separately)

## Technologies Used

- **Google ADK**: Agent Development Kit for building AI agents
- **FastMCP**: Model Context Protocol server framework
- **LiteLLM**: Unified LLM API interface
- **Ollama**: Local LLM inference with Llama 3.2
- **Docker & Docker Compose**: Containerization and orchestration