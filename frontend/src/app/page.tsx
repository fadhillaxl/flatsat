'use client';

import dynamic from 'next/dynamic';

const TelemetryPanel = dynamic(() => import('@/components/TelemetryPanel'), { ssr: false });
const CameraPanel = dynamic(() => import('@/components/CameraPanel'), { ssr: false });
const RelayControl = dynamic(() => import('@/components/RelayControl'), { ssr: false });
const SDRPanel = dynamic(() => import('@/components/SDRPanel'), { ssr: false });
const SystemStatus = dynamic(() => import('@/components/SystemStatus'), { ssr: false });

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white p-4 font-mono">
      <header className="mb-6 border-b border-gray-700 pb-4">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-blue-500">FLATSAT MISSION CONTROL</h1>
            <div className="text-sm text-gray-400">Status: CONNECTED | Link: LOCALHOST</div>
          </div>
          <SystemStatus />
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Telemetry & Relays */}
        <div className="space-y-6">
          <section>
            <h2 className="text-xl font-bold mb-2 text-green-400 border-l-4 border-green-400 pl-2">
              TELEMETRY & AVIONICS
            </h2>
            <TelemetryPanel />
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2 text-yellow-400 border-l-4 border-yellow-400 pl-2">
              POWER DISTRIBUTION
            </h2>
            <RelayControl />
          </section>
        </div>

        {/* Right Column: Payload & SDR */}
        <div className="space-y-6">
          <section>
            <h2 className="text-xl font-bold mb-2 text-purple-400 border-l-4 border-purple-400 pl-2">
              CAMERA PAYLOAD
            </h2>
            <CameraPanel />
          </section>

          <section>
            <h2 className="text-xl font-bold mb-2 text-red-400 border-l-4 border-red-400 pl-2">
              RF & SDR PAYLOAD
            </h2>
            <SDRPanel />
          </section>
        </div>
      </div>
    </main>
  );
}
