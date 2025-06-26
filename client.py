import asyncio
from fastmcp import Client

client = Client("/Users/siddasha/mcp_test/test/testmcp.py")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("create_api_client", {"language": "Python", "spec_ref": "https://github.com/backstage/backstage/blob/master/plugins/api-docs/dev/openapi-example-api.yaml"})
        print(result)


asyncio.run(call_tool("Ford"))