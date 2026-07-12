import { useState, useEffect } from 'react';
import { BarChart2, Clock, CheckCircle, AlertCircle, ChevronRight, RefreshCw, User } from 'lucide-react';
import CaseDetailsModal from './CaseDetailsModal';

const statusColors = {
  'Submitted':  'bg-yellow-100 text-yellow-800 border-yellow-200',
  'In Review':  'bg-blue-100 text-blue-800 border-blue-200',
  'Approved':   'bg-emerald-100 text-emerald-800 border-emerald-200',
  'Closed':     'bg-slate-100 text-slate-600 border-slate-200',
};

export default function Queue() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCase, setSelectedCase] = useState(null);
  const [filter, setFilter] = useState('All');

  const fetchCases = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/cases');
      if (res.ok) setCases(await res.json());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchCases(); }, []);

  const stats = {
    total: cases.length,
    pending: cases.filter(c => c.status === 'Submitted').length,
    inReview: cases.filter(c => c.status === 'In Review').length,
    approved: cases.filter(c => c.status === 'Approved').length,
  };

  const filtered = filter === 'All' ? cases : cases.filter(c => c.status === filter);

  return (
    <>
      {/* Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: 'Total Cases', value: stats.total, icon: BarChart2, color: 'text-slate-600', bg: 'bg-slate-100' },
          { label: 'Pending Review', value: stats.pending, icon: Clock, color: 'text-yellow-600', bg: 'bg-yellow-50' },
          { label: 'In Review', value: stats.inReview, icon: AlertCircle, color: 'text-blue-600', bg: 'bg-blue-50' },
          { label: 'Approved FIRs', value: stats.approved, icon: CheckCircle, color: 'text-emerald-600', bg: 'bg-emerald-50' },
        ].map(({ label, value, icon: Icon, color, bg }) => (
          <div key={label} className="bg-white rounded-xl p-5 shadow-sm border border-slate-100 flex items-center gap-4">
            <div className={`p-3 rounded-xl ${bg}`}>
              <Icon className={`w-6 h-6 ${color}`} />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-800">{value}</p>
              <p className="text-xs text-slate-500">{label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Filters & Refresh */}
      <div className="flex flex-wrap gap-2 mb-5 items-center justify-between">
        <div className="flex gap-2">
          {['All', 'Submitted', 'In Review', 'Approved', 'Closed'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition border ${
                filter === f ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-600 border-slate-200 hover:border-slate-400'
              }`}
            >
              {f}
            </button>
          ))}
        </div>
        <button onClick={fetchCases} className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-600 hover:border-slate-400 text-sm transition">
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
      </div>

      {/* Case List */}
      {loading ? (
        <div className="text-center py-20 text-slate-400">Loading cases...</div>
      ) : filtered.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-xl border border-slate-100 text-slate-400">
          No cases found for "{filter}" filter.
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map(c => (
            <div
              key={c.case_id}
              onClick={() => setSelectedCase(c)}
              className="bg-white rounded-xl border border-slate-100 shadow-sm p-5 flex items-center gap-4 cursor-pointer hover:border-slate-300 hover:shadow-md transition group"
            >
              <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center shrink-0">
                <User className="w-5 h-5 text-slate-500" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 mb-1">
                  <span className="font-bold text-slate-800 font-mono text-sm">{c.case_id}</span>
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium border ${statusColors[c.status] || 'bg-slate-100 text-slate-600'}`}>
                    {c.status}
                  </span>
                </div>
                <p className="text-slate-700 font-medium truncate">{c.subject}</p>
                <div className="flex gap-3 mt-1 text-xs text-slate-400">
                  <span>{c.citizen_username}</span>
                  <span>·</span>
                  <span>{c.category}</span>
                  <span>·</span>
                  <span>{new Date(c.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              {c.suggested_section && (
                <div className="hidden md:block text-xs text-indigo-700 bg-indigo-50 px-3 py-2 rounded-lg max-w-[200px] truncate border border-indigo-100">
                  {c.suggested_section}
                </div>
              )}
              <ChevronRight className="w-5 h-5 text-slate-300 group-hover:text-slate-500 transition shrink-0" />
            </div>
          ))}
        </div>
      )}

      {selectedCase && (
        <CaseDetailsModal
          caseData={selectedCase}
          onClose={() => setSelectedCase(null)}
          onUpdate={fetchCases}
        />
      )}
    </>
  );
}
