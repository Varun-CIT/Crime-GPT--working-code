import { useState } from 'react';
import SubmitComplaint from './SubmitComplaint';
import TrackCase from './TrackCase';
import { Shield } from 'lucide-react';

function App() {
  const [activeTab, setActiveTab] = useState('submit');

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <div className="bg-red-600 text-white py-2 text-center text-sm font-bold tracking-wide">
        🚨 FOR EMERGENCIES, CALL 112 IMMEDIATELY 🚨
      </div>
      
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 text-blue-900 font-bold text-xl">
            <Shield className="w-8 h-8" />
            <span>CrimeGPT Portal</span>
          </div>
          <nav className="flex gap-4">
            <button 
              onClick={() => setActiveTab('submit')}
              className={`px-4 py-2 rounded-lg font-medium transition ${activeTab === 'submit' ? 'bg-blue-50 text-blue-900' : 'text-slate-600 hover:bg-slate-100'}`}
            >
              Lodge Complaint
            </button>
            <button 
              onClick={() => setActiveTab('track')}
              className={`px-4 py-2 rounded-lg font-medium transition ${activeTab === 'track' ? 'bg-blue-50 text-blue-900' : 'text-slate-600 hover:bg-slate-100'}`}
            >
              Track Status
            </button>
          </nav>
        </div>
      </header>

      <main className="p-6">
        {activeTab === 'submit' ? <SubmitComplaint /> : <TrackCase />}
      </main>
    </div>
  );
}

export default App;
