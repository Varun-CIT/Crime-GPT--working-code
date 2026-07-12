import { useState } from 'react';
import { Search, Clock, FileText, CheckCircle2, ChevronRight } from 'lucide-react';

export default function TrackCase() {
  const [searchId, setSearchId] = useState('');
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchId) return;
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/api/cases');
      if (res.ok) {
        const cases = await res.json();
        const found = cases.find(c => c.case_id === searchId);
        if (found) {
          setCaseData(found);
        } else {
          setError('Case not found. Please check your Case ID.');
          setCaseData(null);
        }
      } else {
        setError('Failed to fetch cases from server.');
      }
    } catch (err) {
      setError('Network error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-8">
      <div className="bg-white rounded-xl shadow-sm overflow-hidden mb-6">
        <div className="p-6">
          <h2 className="text-xl font-bold text-slate-800 mb-4 flex items-center gap-2">
            <Search className="w-6 h-6 text-blue-900" /> Track Case Status
          </h2>
          <form onSubmit={handleSearch} className="flex gap-3">
            <input 
              type="text" 
              value={searchId} 
              onChange={e => setSearchId(e.target.value)} 
              placeholder="Enter Case ID (e.g. CGPT-2026-0001)" 
              className="flex-1 px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-900 focus:outline-none text-lg"
            />
            <button type="submit" disabled={loading} className="px-8 bg-blue-900 text-white font-semibold rounded-lg hover:bg-blue-800 transition">
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
          {error && <p className="text-red-600 mt-3">{error}</p>}
        </div>
      </div>

      {caseData && (
        <div className="grid md:grid-cols-3 gap-6">
          {/* Main details */}
          <div className="md:col-span-2 space-y-6">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold text-slate-800">{caseData.case_id}</h3>
                  <p className="text-slate-500">{caseData.subject}</p>
                </div>
                <span className="px-4 py-1 bg-blue-100 text-blue-800 rounded-full font-medium border border-blue-200">
                  {caseData.status}
                </span>
              </div>
              
              <div className="space-y-4">
                <div className="flex gap-4 p-4 bg-slate-50 rounded-lg">
                  <div className="w-1/3 text-sm text-slate-500">Citizen</div>
                  <div className="w-2/3 font-medium text-slate-800">{caseData.citizen_username}</div>
                </div>
                <div className="flex gap-4 p-4 bg-slate-50 rounded-lg">
                  <div className="w-1/3 text-sm text-slate-500">Category</div>
                  <div className="w-2/3 font-medium text-slate-800">{caseData.category}</div>
                </div>
                <div className="flex gap-4 p-4 bg-slate-50 rounded-lg">
                  <div className="w-1/3 text-sm text-slate-500">Description / Transcript</div>
                  <div className="w-2/3 text-slate-700 italic">"{caseData.description}"</div>
                </div>
              </div>
            </div>

            {/* AI Extracted Data */}
            {caseData.fir_json && (
              <div className="bg-white rounded-xl shadow-sm p-6 border-l-4 border-indigo-500">
                <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2 mb-4">
                  <FileText className="w-5 h-5 text-indigo-500" />
                  AI Legal Breakdown
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-slate-600">Cognizable Offense:</span>
                    <span className="font-semibold text-slate-800">{caseData.cognizable ? 'Yes' : 'No'}</span>
                  </div>
                  <div>
                    <span className="text-slate-600 block mb-1">Suggested BNS 2023 Sections:</span>
                    <div className="bg-indigo-50 p-3 rounded text-indigo-900 font-medium">
                      {caseData.suggested_section || 'Pending Officer Review'}
                    </div>
                  </div>
                  {/* Parse FIR Draft details if possible */}
                  <details className="mt-4 group">
                    <summary className="cursor-pointer text-indigo-600 font-medium list-none flex items-center justify-between p-3 bg-slate-50 rounded-lg">
                      View Raw AI Draft
                      <ChevronRight className="w-5 h-5 group-open:rotate-90 transition" />
                    </summary>
                    <pre className="mt-2 p-4 bg-slate-800 text-slate-200 text-xs rounded-lg overflow-x-auto">
                      {JSON.stringify(JSON.parse(caseData.fir_json), null, 2)}
                    </pre>
                  </details>
                </div>
              </div>
            )}
          </div>

          {/* Timeline side panel */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h3 className="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
              <Clock className="w-5 h-5" /> Timeline
            </h3>
            
            <div className="relative border-l-2 border-slate-200 ml-3 space-y-8">
              {/* Submitted Step */}
              <div className="relative pl-6">
                <div className="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-emerald-500 border-2 border-white ring-2 ring-emerald-100"></div>
                <h4 className="font-bold text-slate-800">Submitted</h4>
                <p className="text-xs text-slate-500">{new Date(caseData.created_at).toLocaleString()}</p>
              </div>

              {/* In Review Step */}
              <div className="relative pl-6">
                <div className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full border-2 border-white ${caseData.status !== 'Submitted' ? 'bg-emerald-500 ring-2 ring-emerald-100' : 'bg-slate-300'}`}></div>
                <h4 className={`font-bold ${caseData.status !== 'Submitted' ? 'text-slate-800' : 'text-slate-400'}`}>In Review</h4>
                {caseData.status !== 'Submitted' && <p className="text-xs text-slate-500 mt-1">Officer Assigned</p>}
              </div>

              {/* Approved/Closed Step */}
              <div className="relative pl-6">
                <div className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full border-2 border-white ${caseData.status === 'Approved' || caseData.status === 'Closed' ? 'bg-blue-600 ring-2 ring-blue-100' : 'bg-slate-300'}`}></div>
                <h4 className={`font-bold ${caseData.status === 'Approved' || caseData.status === 'Closed' ? 'text-blue-600' : 'text-slate-400'}`}>
                  {caseData.status === 'Closed' ? 'Closed' : 'FIR Approved'}
                </h4>
                {(caseData.status === 'Approved' || caseData.status === 'Closed') && 
                  <p className="text-xs text-slate-500 mt-1">{new Date(caseData.updated_at).toLocaleString()}</p>
                }
              </div>
            </div>
          </div>

        </div>
      )}
    </div>
  );
}
