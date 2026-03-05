'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

const API_URL = 'http://localhost:8000';

export default function SDRPanel() {
  const [sdrStatus, setSdrStatus] = useState<any>(null);
  const [spectrumData, setSpectrumData] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSDRStatus();
    const interval = setInterval(() => {
      fetchSpectrum();
    }, 500);
    return () => clearInterval(interval);
  }, []);

  const fetchSDRStatus = async () => {
    try {
      const res = await axios.get(`${API_URL}/sdr/status`);
      setSdrStatus(res.data);
      setLoading(false);
    } catch (err) {
      console.error("Failed to fetch SDR status", err);
    }
  };

  const fetchSpectrum = async () => {
    try {
      const res = await axios.get(`${API_URL}/spectrum`);
      setSpectrumData(res.data.data);
    } catch (err) {
      console.error("Failed to fetch spectrum", err);
    }
  };

  const toggleTX = async () => {
    if (!sdrStatus) return;
    const newStatus = { ...sdrStatus, tx_enabled: !sdrStatus.tx_enabled };
    try {
      await axios.post(`${API_URL}/sdr/config`, newStatus);
      setSdrStatus(newStatus);
    } catch (err) {
      console.error("Failed to toggle TX", err);
    }
  };

  const toggleRX = async () => {
    if (!sdrStatus) return;
    const newStatus = { ...sdrStatus, rx_enabled: !sdrStatus.rx_enabled };
    try {
      await axios.post(`${API_URL}/sdr/config`, newStatus);
      setSdrStatus(newStatus);
    } catch (err) {
      console.error("Failed to toggle RX", err);
    }
  };

  if (loading) return <div>Loading SDR...</div>;

  const chartData = {
    labels: Array.from({ length: spectrumData.length }, (_, i) => i),
    datasets: [
      {
        label: 'Spectrum (dB)',
        data: spectrumData,
        borderColor: 'rgb(75, 192, 192)',
        borderWidth: 1,
        pointRadius: 0,
        fill: true,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    animation: false as const,
    scales: {
      x: { display: false },
      y: { min: -100, max: 0 },
    },
    plugins: {
      legend: { display: false },
    },
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-900 text-white">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">SDR Payload (ADALM-Pluto)</h2>
        <div className="flex gap-2">
          <button
            onClick={toggleRX}
            className={`px-4 py-2 rounded font-bold ${
              sdrStatus.rx_enabled ? 'bg-green-600' : 'bg-gray-600'
            }`}
          >
            RX {sdrStatus.rx_enabled ? 'ON' : 'OFF'}
          </button>
          <button
            onClick={toggleTX}
            className={`px-4 py-2 rounded font-bold ${
              sdrStatus.tx_enabled ? 'bg-red-600' : 'bg-gray-600'
            }`}
          >
            TX {sdrStatus.tx_enabled ? 'ON' : 'OFF'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
        <div className="bg-gray-800 p-2 rounded">
          <div className="text-gray-400">Frequency</div>
          <div className="text-lg font-mono">{sdrStatus.frequency / 1e6} MHz</div>
        </div>
        <div className="bg-gray-800 p-2 rounded">
          <div className="text-gray-400">Sample Rate</div>
          <div className="text-lg font-mono">{sdrStatus.sample_rate / 1e6} MSPS</div>
        </div>
        <div className="bg-gray-800 p-2 rounded">
          <div className="text-gray-400">Gain</div>
          <div className="text-lg font-mono">{sdrStatus.gain} dB</div>
        </div>
      </div>

      <div className="h-48 bg-black rounded border border-gray-700 p-2">
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
}
