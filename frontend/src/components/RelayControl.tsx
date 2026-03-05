'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export default function RelayControl() {
  const [relays, setRelays] = useState<boolean[]>([false, false, false, false]);

  useEffect(() => {
    fetchRelays();
  }, []);

  const fetchRelays = async () => {
    try {
      const res = await axios.get(`${API_URL}/relays`);
      setRelays(res.data.relays);
    } catch (err) {
      console.error("Failed to fetch relays", err);
    }
  };

  const toggleRelay = async (index: number) => {
    const newState = !relays[index];
    try {
      await axios.post(`${API_URL}/relay/${index + 1}/${newState ? 'on' : 'off'}`);
      const newRelays = [...relays];
      newRelays[index] = newState;
      setRelays(newRelays);
    } catch (err) {
      console.error("Failed to toggle relay", err);
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-900 text-white">
      <h2 className="text-xl font-bold mb-4">Relay Control</h2>
      <div className="grid grid-cols-2 gap-4">
        {relays.map((isOn, idx) => (
          <div key={idx} className="flex items-center justify-between p-2 bg-gray-800 rounded">
            <span>Relay {idx + 1}</span>
            <button
              onClick={() => toggleRelay(idx)}
              className={`px-4 py-2 rounded font-bold ${
                isOn ? 'bg-green-500 hover:bg-green-600' : 'bg-red-500 hover:bg-red-600'
              }`}
            >
              {isOn ? 'ON' : 'OFF'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
