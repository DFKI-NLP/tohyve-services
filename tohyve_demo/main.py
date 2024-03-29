import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from websockets.exceptions import ConnectionClosedError
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from websocket_ import ConnectionManager

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the directory containing your HTML files
templates = Jinja2Templates(directory="templates")

manager = ConnectionManager()


# Endpoint to serve the HTML file
@app.get("/tohyve-demo",response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Endpoint for the websocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    collected_messages = []
    try:
        while True:
            json_data = await websocket.receive_text()
                        
            asr_response, asr_succ, src, trg, file_upload = await manager.get_asr(json_data)

            if (await manager.is_full_text(asr_response) and len(collected_messages)>0) or file_upload:
                collected_messages.append(asr_response)
                asr_responses = " ".join(collected_messages)
                collected_messages = []
                await manager.send_personal_message(websocket, asr_responses, asr_succ, src, trg)
                
            else:
                collected_messages.append(asr_response)


    except WebSocketDisconnect as e:
        await manager.disconnect(websocket)
    
    except ConnectionClosedError as e:
        if e.code == 1011:
            # Handle the specific error code 1011 (unexpected error)
            print(f"ConnectionClosedError: {e}")

    except Exception as e:
        # Handle other exceptions
        print(f"Unexpected error: {e}")


# Start the WebSocket server in a separate thread
if __name__ == '__main__':
        uvicorn.run(
        "main:app",
        host    = "0.0.0.0",
        port    = 8005
    )
        
