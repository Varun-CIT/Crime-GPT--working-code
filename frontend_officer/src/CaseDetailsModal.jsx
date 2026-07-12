import { useState, useEffect, useRef } from 'react';
import { X, User, Phone, FileText, Shield, CheckCircle, Clock, ChevronDown, AlertTriangle } from 'lucide-react';

export default function CaseDetailsModal({ caseData, onClose, onUpdate }) {
  const [status, setStatus] = useState(caseData.status || 'Submitted');
  const [remarks, setRemarks] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const modalRef = useRef(null);

  const firData = caseData.fir_json ? JSON.parse(caseData.fir_json) : null;

  const statuses = ['Submitted', 'In Review', 'Approved', 'Closed'];

  const statusColors = {
    'Submitted':  'bg-yellow-100 text-yellow-800',
    'In Review':  'bg-blue-100 text-blue-800',
    'Approved':   'bg-emerald-100 text-emerald-800',
    'Closed':     'bg-slate-100 text-slate-700',
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/cases/${caseData.case_id}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, remarks, officer_username: 'Inspector Rajesh' })
      });
      if (res.ok) {
        setSuccess(true);
        setTimeout(() => { onUpdate(); onClose(); }, 1500);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex" onClick={e => { if (modalRef.current && !modalRef.current.contains(e.target)) onClose(); }}>
      <div className="flex-1 bg-black/40 backdrop-blur-sm" />
      <div ref={modalRef} className="w-full max-w-2xl bg-white shadow-2xl h-full overflow-y-auto animate-slide-in">
        {/* Header */}
        <div className="sticky top-0 bg-slate-900 text-white p-5 flex items-start justify-between z-10">
          <div>
            <p className="text-slate-400 text-xs uppercase tracking-widest font-medium">Case Review</p>
            <h2 className="text-xl font-bold mt-1">{caseData.case_id}</h2>
            <p className="text-slate-300 text-sm mt-1">{caseData.subject}</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-lg transition"><X className="w-5 h-5"/></button>
        </div>

        <div className="p-6 space-y-6">
          {/* Citizen Info */}
          <div className="bg-slate-50 rounded-xl p-4 space-y-3">
            <h3 className="font-semibold text-slate-700 text-sm uppercase tracking-wide">Citizen Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center gap-2 text-slate-700">
                <User className="w-4 h-4 text-slate-400" />
                <span className="text-sm">{caseData.citizen_username}</span>
              </div>
              <div className="flex items-center gap-2 text-slate-700">
                <Phone className="w-4 h-4 text-slate-400" />
                <span className="text-sm">{caseData.citizen_phone}</span>
              </div>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-1">Category</p>
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">{caseData.category}</span>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-1">Complaint / Transcript</p>
              <p className="text-sm text-slate-700 leading-relaxed italic">"{caseData.description}"</p>
            </div>
          </div>

          {/* AI Analysis */}
          {firData ? (
            <div className="border border-indigo-200 rounded-xl overflow-hidden">
              <div className="bg-indigo-600 text-white px-4 py-3 flex items-center gap-2">
                <Shield className="w-4 h-4" />
                <span className="font-semibold text-sm">AI Legal Analysis</span>
                <span className="ml-auto px-2 py-0.5 bg-white/20 rounded text-xs">BNS 2023</span>
              </div>
              <div className="p-4 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-600">Cognizable Offense</span>
                  <span className={`px-3 py-0.5 rounded-full text-xs font-bold ${caseData.cognizable ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-600'}`}>
                    {caseData.cognizable ? 'YES — FIR Required' : 'NO — NC Entry'}
                  </span>
                </div>
                <div>
                  <p className="text-sm text-slate-600 mb-1">Recommended Sections</p>
                  <div className="flex flex-wrap gap-2">
                    {(caseData.suggested_section || '').split(',').map((s, i) => (
                      <span key={i} className="px-3 py-1 bg-indigo-50 text-indigo-700 rounded-full text-xs font-medium border border-indigo-200">
                        {s.trim()}
                      </span>
                    ))}
                  </div>
                </div>
                {firData.incident_summary && (
                  <div>
                    <p className="text-xs text-slate-500 mb-1">AI Incident Summary</p>
                    <p className="text-sm text-slate-700 bg-slate-50 p-3 rounded">{firData.incident_summary}</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex items-center gap-3 p-4 bg-amber-50 border border-amber-200 rounded-xl text-amber-700">
              <AlertTriangle className="w-5 h-5 shrink-0" />
              <span className="text-sm">AI analysis not available. OpenAI key may not be configured.</span>
            </div>
          )}

          {/* Status Control */}
          <div className="space-y-4">
            <h3 className="font-semibold text-slate-700 text-sm uppercase tracking-wide">Update Case Status</h3>
            <div className="relative">
              <select
                value={status}
                onChange={e => setStatus(e.target.value)}
                className="w-full appearance-none px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-800 focus:outline-none bg-white font-medium pr-10"
              >
                {statuses.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
              <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" />
            </div>
            <textarea
              value={remarks}
              onChange={e => setRemarks(e.target.value)}
              placeholder="Add official remarks or action notes..."
              className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-slate-800 focus:outline-none h-24 resize-none"
            />
          </div>

          {/* Submit */}
          <div className="flex gap-3">
            <button onClick={onClose} className="flex-1 py-3 border-2 border-slate-200 rounded-xl font-semibold text-slate-600 hover:bg-slate-100 transition">
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              disabled={loading || success}
              className="flex-1 py-3 bg-slate-900 text-white rounded-xl font-semibold hover:bg-slate-800 transition disabled:opacity-70 flex items-center justify-center gap-2"
            >
              {success ? (
                <><CheckCircle className="w-5 h-5 text-emerald-400" /> Logged to Audit Chain</>
              ) : loading ? (
                <><div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> Submitting...</>
              ) : (
                <><Shield className="w-5 h-5" /> Submit Review</>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
