import uvicorn

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from websocket_ import ConnectionManager

app = FastAPI()


# Mount the directory containing your HTML files
# app.mount("/static", StaticFiles(directory="./templates", html=True), name="static")
templates = Jinja2Templates(directory="templates")



manager = ConnectionManager()

@app.get("/tohyve-demo",response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
        

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            json_data = await websocket.receive_text()
            await manager.send_personal_message(json_data, websocket)  
    except WebSocketDisconnect:
        manager.disconnect(websocket)






# Start the WebSocket server in a separate thread
if __name__ == '__main__':
        uvicorn.run(
        "main:app",
        host    = "0.0.0.0",
        port    = 8005
    )