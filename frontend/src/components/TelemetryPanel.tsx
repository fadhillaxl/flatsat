'use client';

import { useEffect, useState } from 'react';
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
import axios from 'axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_URL = 'http://localhost:8000';

export default function TelemetryPanel() {
  const [telemetry, setTelemetry] = useState<any>(null);
  const [history, setHistory] = useState<{
    labels: string[];
    voltage: number[];
    current: number[];
    accelX: number[];
    accelY: number[];
    accelZ: number[];
  }>({
    labels: [],
    voltage: [],
    current: [],
    accelX: [],
    accelY: [],
    accelZ: [],
  });

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`${API_URL}/telemetry`);
        const data = res.data;
        setTelemetry(data);

        setHistory((prev) => {
          const newLabels = [...prev.labels, new Date().toLocaleTimeString()].slice(-20);
          const newVoltage = [...prev.voltage, data.power.voltage].slice(-20);
          const newCurrent = [...prev.current, data.power.current].slice(-20);
          const newAccelX = [...prev.accelX, data.imu.accel.x].slice(-20);
          const newAccelY = [...prev.accelY, data.imu.accel.y].slice(-20);
          const newAccelZ = [...prev.accelZ, data.imu.accel.z].slice(-20);

          return {
            labels: newLabels,
            voltage: newVoltage,
            current: newCurrent,
            accelX: newAccelX,
            accelY: newAccelY,
            accelZ: newAccelZ,
          };
        });
      } catch (err) {
        console.error("Failed to fetch telemetry", err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  if (!telemetry) return <div className="p-4">Loading Telemetry...</div>;

  const powerData = {
    labels: history.labels,
    datasets: [
      {
        label: 'Voltage (V)',
        data: history.voltage,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        yAxisID: 'y',
      },
      {
        label: 'Current (mA)',
        data: history.current,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
        yAxisID: 'y1',
      },
    ],
  };

  const imuData = {
    labels: history.labels,
    datasets: [
      {
        label: 'Accel X',
        data: history.accelX,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Accel Y',
        data: history.accelY,
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
      {
        label: 'Accel Z',
        data: history.accelZ,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    interaction: {
      mode: 'index' as const,
      intersect: false,
    },
    stacked: false,
    scales: {
      y: {
        type: 'linear' as const,
        display: true,
        position: 'left' as const,
        title: { display: true, text: 'Voltage (V)' }
      },
      y1: {
        type: 'linear' as const,
        display: true,
        position: 'right' as const,
        grid: {
          drawOnChartArea: false,
        },
        title: { display: true, text: 'Current (mA)' }
      },
    },
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 border rounded-lg bg-gray-900 text-white">
      <div className="col-span-2 text-xl font-bold mb-2">Telemetry</div>
      
      <div className="bg-gray-800 p-2 rounded">
        <h3 className="text-lg mb-2">Power System</h3>
        <div className="grid grid-cols-3 gap-2 mb-2 text-sm">
           <div>Voltage: {telemetry.power.voltage} V</div>
           <div>Current: {telemetry.power.current} mA</div>
           <div>Power: {telemetry.power.power} W</div>
        </div>
        <Line options={options} data={powerData} />
      </div>

      <div className="bg-gray-800 p-2 rounded">
        <h3 className="text-lg mb-2">IMU Sensor</h3>
        <div className="grid grid-cols-3 gap-2 mb-2 text-sm">
           <div>Roll: {telemetry.imu.roll}°</div>
           <div>Pitch: {telemetry.imu.pitch}°</div>
           <div>Yaw: {telemetry.imu.yaw}°</div>
        </div>
        <Line options={{...options, scales: {}}} data={imuData} />
      </div>
      
      <div className="col-span-2 bg-gray-800 p-2 rounded">
         <div className="flex justify-between mb-2 font-bold">
            <span>System Status</span>
            <span>Uptime: {telemetry.system.uptime}s</span>
         </div>
         <div className="grid grid-cols-3 gap-4 text-sm border-t border-gray-700 pt-2">
            <div>
              <div className="text-gray-400 font-semibold mb-1">Compute Load</div>
              <div className="flex justify-between"><span>CPU:</span> <span>{telemetry.system.cpu_usage}%</span></div>
              <div className="flex justify-between"><span>RAM:</span> <span>{telemetry.system.ram_usage}%</span></div>
              <div className="flex justify-between"><span>Disk:</span> <span>{telemetry.system.disk_usage}%</span></div>
            </div>
            <div>
              <div className="text-gray-400 font-semibold mb-1">Environment</div>
              <div className="flex justify-between"><span>Ext Temp:</span> <span>{telemetry.environment.temperature}°C</span></div>
              <div className="flex justify-between"><span>CPU Temp:</span> <span>{telemetry.system.cpu_temp}°C</span></div>
              <div className="flex justify-between"><span>Humidity:</span> <span>{telemetry.environment.humidity}%</span></div>
            </div>
            <div>
              <div className="text-gray-400 font-semibold mb-1">Atmosphere</div>
              <div className="flex justify-between"><span>Pressure:</span> <span>{telemetry.environment.pressure} hPa</span></div>
              <div className="flex justify-between"><span>Altitude:</span> <span>{telemetry.environment.altitude} m</span></div>
            </div>
         </div>
      </div>
    </div>
  );
}
