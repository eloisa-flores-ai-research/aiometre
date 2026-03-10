import asyncio
import websockets
import json
import os
import base64
from google import genai
from google.genai import types

API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = "You are AIOmetre, a warm human connection companion. Always respond naturally and warmly."

async def handle_client(websocket):
    try:
        client = genai.Client(api_key=API_KEY, http_options={"api_version": "v1alpha"})
        config = types.LiveConnectConfig(response_modalities=["TEXT"])
        async with client.aio.live.connect(model="gemini-2.0-flash-live-001", config=config) as session:
            async def receive_from_client():
                async for message in websocket:
                    data = json.loads(message)
                    if "text" in data:
                        await session.send(input=data["text"], end_of_turn=True)
            async def send_to_client():
                async for response in session.receive():
                    if response.text:
                        await websocket.send(json.dumps({"type": "text", "text": response.text}))
            await asyncio.gather(receive_from_client(), send_to_client())
    except Exception as e:
        await websocket.send(json.dumps({"type": "error", "text": str(e)}))

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8081):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
