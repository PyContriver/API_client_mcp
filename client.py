import asyncio
import os
from fastmcp import Client

mcp_file_path = os.environ.get("server_file_path")
client = Client(mcp_file_path)

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("create_api_client", {"language": "Python", "spec_ref": "https://github.com/backstage/backstage/blob/master/plugins/api-docs/dev/openapi-example-api.yaml"})
        print(result)


asyncio.run(call_tool("Ford"))
