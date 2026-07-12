import { useState } from 'react';
import Queue from './Queue';
import CitationVerifier from './CitationVerifier';
import { LayoutDashboard, Scale, ShieldCheck, LogOut } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('queue');

  const navItems = [
    { id: 'queue', label: 'Case Queue', icon: LayoutDashboard },
    { id: 'citations', label: 'Citation Verifier', icon: Scale },
  ];

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-white flex flex-col shrink-0 fixed h-full">
        {/* Logo */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-2.5">
            <ShieldCheck className="w-8 h-8 text-blue-400" />
            <div>
              <p className="font-bold text-white">CrimeGPT</p>
              <p className="text-xs text-slate-400">Officer Command Center</p>
            </div>
          </div>
        </div>

        {/* Officer Badge */}
        <div className="p-4 m-4 bg-white/5 rounded-xl border border-white/10">
          <p className="text-xs text-slate-400 uppercase tracking-widest font-medium mb-1">Active Officer</p>
          <p className="font-semibold text-white">Inspector Rajesh</p>
          <p className="text-xs text-blue-400 mt-0.5">Cyber Crime Unit · TN</p>
        </div>

        {/* Nav Links */}
        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition ${
                activeTab === id
                  ? 'bg-white text-slate-900'
                  : 'text-slate-400 hover:bg-white/10 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5" />
              {label}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-white/10">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm text-slate-500 hover:text-white hover:bg-white/10 transition">
            <LogOut className="w-5 h-5" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Area */}
      <main className="flex-1 ml-64">
        <div className="p-8">
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-slate-800">
              {activeTab === 'queue' ? 'Complaint Queue' : 'Legal Citation Verifier'}
            </h1>
            <p className="text-slate-500 text-sm mt-1">
              {activeTab === 'queue'
                ? 'Review AI-processed complaints and update case statuses.'
                : 'Cross-reference case law citations cited in AI-generated FIR drafts.'}
            </p>
          </div>
          {activeTab === 'queue' ? <Queue /> : <CitationVerifier />}
        </div>
      </main>
    </div>
  );
}
