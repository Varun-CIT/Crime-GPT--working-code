import { useState } from 'react';
import { Search, CheckCircle, AlertTriangle, XCircle, Scale } from 'lucide-react';

export default function CitationVerifier() {
  const [citation, setCitation] = useState('');
  const [quote, setQuote] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleVerify = async () => {
    if (!citation) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('http://127.0.0.1:8000/api/verify_citation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ citation_text: citation, quoted_paragraph: quote })
      });
      if (res.ok) setResult(await res.json());
    } catch (err) {
      setResult({ verdict: 'Error', explanation: 'Network error. Is the backend running?' });
    } finally {
      setLoading(false);
    }
  };

  const verdictConfig = {
    'Verified': { icon: CheckCircle, cls: 'border-emerald-200 bg-emerald-50 text-emerald-800', iconCls: 'text-emerald-500' },
    'Suspicious': { icon: AlertTriangle, cls: 'border-amber-200 bg-amber-50 text-amber-800', iconCls: 'text-amber-500' },
    'Hallucinated': { icon: XCircle, cls: 'border-red-200 bg-red-50 text-red-800', iconCls: 'text-red-500' },
    'Error': { icon: XCircle, cls: 'border-red-200 bg-red-50 text-red-800', iconCls: 'text-red-500' },
  };

  const config = result ? (verdictConfig[result.verdict] || verdictConfig['Error']) : null;

  return (
    <div className="max-w-2xl">
      <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex items-center gap-3">
          <div className="p-2.5 bg-indigo-50 rounded-xl">
            <Scale className="w-6 h-6 text-indigo-600" />
          </div>
          <div>
            <h2 className="font-bold text-slate-800 text-lg">Legal Citation Verifier</h2>
            <p className="text-sm text-slate-500">Cross-reference AI case law to prevent hallucinations</p>
          </div>
        </div>

        <div className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Citation String</label>
            <input
              type="text"
              value={citation}
              onChange={e => setCitation(e.target.value)}
              placeholder="e.g. AIR 2021 SC 4521 or BNS Section 61"
              className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">Quoted Paragraph (Optional)</label>
            <textarea
              value={quote}
              onChange={e => setQuote(e.target.value)}
              placeholder="Paste the quote you want to verify..."
              className="w-full px-4 py-3 border-2 border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none h-28 resize-none transition"
            />
          </div>
          <button
            onClick={handleVerify}
            disabled={loading || !citation}
            className="w-full py-3 bg-indigo-600 text-white font-semibold rounded-xl hover:bg-indigo-700 transition disabled:opacity-60 flex justify-center items-center gap-2"
          >
            {loading ? (
              <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" /> Verifying...</>
            ) : (
              <><Search className="w-5 h-5" /> Verify Citation</>
            )}
          </button>
        </div>
      </div>

      {result && config && (
        <div className={`mt-6 border-2 rounded-xl p-6 ${config.cls}`}>
          <div className="flex items-center gap-3 mb-3">
            <config.icon className={`w-8 h-8 ${config.iconCls}`} />
            <h3 className="text-xl font-bold">{result.verdict}</h3>
          </div>
          <p className="text-sm leading-relaxed">{result.explanation}</p>
          {result.closest_match && (
            <div className="mt-4 p-3 bg-white/70 rounded-lg border">
              <p className="text-xs font-semibold uppercase mb-1 text-slate-600">Closest Known Reference</p>
              <p className="text-sm font-mono">{result.closest_match}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
