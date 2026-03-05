'use client';

import { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000';

export default function CameraPanel() {
  const [timestamp, setTimestamp] = useState(Date.now());
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(() => {
        setTimestamp(Date.now());
      }, 1000); // Refresh every second
    }
    return () => clearInterval(interval);
  }, [autoRefresh]);

  return (
    <div className="p-4 border rounded-lg bg-gray-900 text-white">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Camera Payload</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`px-3 py-1 rounded text-sm ${
              autoRefresh ? 'bg-green-600' : 'bg-gray-600'
            }`}
          >
            {autoRefresh ? 'Streaming' : 'Paused'}
          </button>
          <button
            onClick={() => setTimestamp(Date.now())}
            className="px-3 py-1 bg-blue-600 rounded text-sm hover:bg-blue-700"
          >
            Capture
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[0, 1, 2].map((id) => (
          <div key={id} className="relative bg-black aspect-video rounded overflow-hidden border border-gray-700">
            <img
              src={`${API_URL}/camera/${id}?t=${timestamp}`}
              alt={`Camera ${id}`}
              className="w-full h-full object-cover"
            />
            <div className="absolute top-2 left-2 bg-black/50 px-2 py-1 rounded text-xs">
              CAM {id}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
