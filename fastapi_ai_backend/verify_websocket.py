import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected! Waiting for refresh signal...")
            # Wait for at least one message
            message = await websocket.recv()
            print(f"Received: {message}")
            if message == "refresh":
                print("[OK] WebSocket test passed!")
            else:
                print(f"[FAIL] Unexpected message: {message}")
    except Exception as e:
        print(f"[FAIL] Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket())
