'use client';

import { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default function SystemStatus() {
  const [status, setStatus] = useState<Record<string, string>>({});

  useEffect(() => {
    axios.get(`${API_URL}/status`)
      .then(res => setStatus(res.data))
      .catch(err => console.error("Failed to fetch status", err));
  }, []);

  return (
    <div className="flex gap-4 text-xs mt-2">
      {Object.entries(status).map(([key, value]) => (
        <div key={key} className={`px-2 py-1 rounded border ${
          value === 'REAL' ? 'border-green-500 text-green-500 bg-green-500/10' : 'border-yellow-500 text-yellow-500 bg-yellow-500/10'
        }`}>
          {key.toUpperCase()}: {value}
        </div>
      ))}
    </div>
  );
}
