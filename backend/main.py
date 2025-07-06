from fastapi import FastAPI, WebSocket
import cv2
import base64
import asyncio
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番ではここを制限したほうが良い
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🟢 WebSocket クライアント接続")

    cap = cv2.VideoCapture(0)

    # ✅ カメラ取得失敗時に終了させる
    if not cap.isOpened():
        print("🔴 カメラが開けません")
        await websocket.close()
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("🔴 フレーム取得失敗")
                break
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_text(jpg_as_text)
            await asyncio.sleep(0.03)
    except Exception as e:
        print("🔴 エラー:", e)
    finally:
        cap.release()
        await websocket.close()
        print("🔵 WebSocket クローズ")

        
@app.get("/")
def read_root():
    return HTMLResponse("""
    <html>
        <body>
            <h1>FastAPI WebSocket サーバー稼働中</h1>
            <p>WebSocket接続は <code>/ws</code> へ。</p>
        </body>
    </html>
    """)
