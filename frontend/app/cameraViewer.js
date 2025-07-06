'use client';
import { useEffect, useRef, useState } from 'react';

const CameraViewer = () => {
  const [imageSrc, setImageSrc] = useState(null);
  const wsRef = useRef(null);

  useEffect(() => {
    // WebSocket接続開始
    const ws = new WebSocket('ws://localhost:8000/ws');
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket接続確立');
    };

    ws.onmessage = (event) => {
      setImageSrc(`data:image/jpeg;base64,${event.data}`);
    };

    ws.onclose = () => {
      console.log('WebSocket切断');
    };

    ws.onerror = (err) => {
      console.error('WebSocketエラー:', err);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div>
      <h2>カメラ映像</h2>
      {imageSrc ? (
        <img src={imageSrc} alt="Camera Stream" style={{ width: '100%', maxWidth: 640 }} />
      ) : (
        <p>読み込み中...</p>
      )}
    </div>
  );
};

export default CameraViewer;
