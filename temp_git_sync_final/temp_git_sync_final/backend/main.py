from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from scanner import ScannerManager

app = FastAPI()

# Enable CORS for local Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scanner = ScannerManager()
event_queue = asyncio.Queue()

class ScanRequest(BaseModel):
    targets: str
    threads: int = 50

@app.post("/scan/start")
async def start_scan(request: ScanRequest):
    """Start the scanning process"""
    targets_list = [line.strip() for line in request.targets.split('\n') if line.strip()]
    if not targets_list:
        return {"status": "error", "message": "No targets provided"}

    # Run in background (non-blocking)
    # Emit start event immediately to UI
    await event_queue.put({"type": "status", "data": "scanning"})
    asyncio.create_task(run_scan_background(targets_list, request.threads))
    return {"status": "started", "count": len(targets_list)}

@app.post("/scan/stop")
async def stop_scan():
    """Stop the current scan"""
    scanner.is_running = False
    return {"status": "stopped"}

@app.get("/events")
async def message_stream(request: Request):
    """Server-Sent Events (SSE) endpoint for real-time updates"""
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            # Get event from queue
            data = await event_queue.get()
            yield json.dumps(data)
            
    return EventSourceResponse(event_generator())

async def run_scan_background(targets, threads):
    """Background task wrapper"""
    # Clear previous queue? Optional.
    
    async def on_result(result):
        # Push result to SSE queue
        await event_queue.put({
            "type": "result",
            "data": result
        })

    # Start event is now handled in the API endpoint for instant feedback
    
    await scanner.run_scan(targets, threads, callback=on_result)
    
    # Push "complete" event
    await event_queue.put({"type": "status", "data": "completed"})

if __name__ == "__main__":
    import uvicorn
    # Run on localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
