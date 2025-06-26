# Before
# from mcp.server.fastmcp import FastMCP

# After
from fastmcp import FastMCP
import requests
import json
import logging

# Set up logging
logger = logging.getLogger("fastmcp")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler("mcp_server.log")
file_handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)


mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

def ask_ollama(prompt):
    url = "http://localhost:11434/api/chat"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    model = "codellama:7b" # UPDATE TO YOUR MODEL
    system_prompt = "You are a helpful api client generator and you will generate a zip file containing the api client code. Do not include any other text in your response."


    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    logging.info(f"Response status code: {response.headers}")


    # Assemble the streamed content
    result = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            result += data.get("message", {}).get("content", "")

    return result.strip()

@mcp.tool
def create_api_client(language, spec_ref) -> str:
    """
    Create an API client based on the provided prompt.
    """
    print(f"Generating API client for {language} with spec {spec_ref}")
    response = ask_ollama(f"Create an API client(zip file) for the following {language} and OpenAPI spec: {spec_ref}")
    if not response:
        print(f"response {response}")
        return f"Failed to generate API client. Please check the model and try again. response {response}"
    return response

if __name__ == "__main__":
    mcp.run()