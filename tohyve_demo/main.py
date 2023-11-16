import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# # from fastapi.staticfiles import StaticFiles
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


# # Mount the "static" directory to serve static files (JavaScript)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount the directory containing your HTML files
templates = Jinja2Templates(directory="templates")

manager = ConnectionManager()

# Endpoint to serve the HTML file
@app.get("/tohyve-demo",response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("sample.html", {"request": request})


# Endpoint for the websocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    collected_messages = []
    try:
        while True:
            json_data = await websocket.receive_text()
            asr_response, asr_succ, src, trg = await manager.get_asr(json_data)
            
            # if asr_succ == False and len(collected_messages) > 0:
            #     asr_responses = " ".join(collected_messages)
            #     await manager.send_personal_message(websocket, asr_responses, asr_succ, src, trg)
            #     collected_messages = []
            # elif asr_succ == False and len(collected_messages) == 0:
            #     await manager.send_personal_message(websocket, asr_response, asr_succ, src, trg)
            #     collected_messages = []
            if await manager.is_full_text(asr_response) and len(collected_messages)>0:
                collected_messages.append(asr_response)
                asr_responses = " ".join(collected_messages)
                collected_messages = []
                await manager.send_personal_message(websocket, asr_responses, asr_succ, src, trg)
                
            else:
                collected_messages.append(asr_response)

    except WebSocketDisconnect:
        manager.disconnect(websocket)




# Start the WebSocket server in a separate thread
if __name__ == '__main__':
        uvicorn.run(
        "main:app",
        host    = "0.0.0.0",
        port    = 8005
    )
        


# https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web