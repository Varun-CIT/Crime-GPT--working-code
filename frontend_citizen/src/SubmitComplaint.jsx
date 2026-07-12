import { useState } from 'react';
import { Upload, Shield, AlertCircle, FileAudio, CheckCircle2 } from 'lucide-react';

export default function SubmitComplaint() {
  const [formData, setFormData] = useState({
    username: '',
    phone: '',
    subject: '',
    category: 'Cyber Fraud',
    description: ''
  });
  const [audioFile, setAudioFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [successId, setSuccessId] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.username || !formData.phone || !formData.subject) {
      setError('Please fill in Name, Phone, and Subject.');
      return;
    }
    
    setLoading(true);
    setError('');
    
    const data = new FormData();
    data.append('citizen_username', formData.username);
    data.append('citizen_phone', formData.phone);
    data.append('subject', formData.subject);
    data.append('category', formData.category);
    data.append('description', formData.description);
    if (audioFile) data.append('audio', audioFile);
    
    try {
      const res = await fetch('http://127.0.0.1:8000/api/cases', {
        method: 'POST',
        body: data
      });
      
      if (res.ok) {
        const json = await res.json();
        setSuccessId(json.case_id);
      } else {
        const err = await res.json();
        setError(err.detail || 'Failed to submit complaint');
      }
    } catch (err) {
      setError('Network error. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  if (successId) {
    return (
      <div className="max-w-2xl mx-auto mt-10 p-8 bg-white rounded-xl shadow-sm text-center">
        <CheckCircle2 className="w-16 h-16 text-emerald-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-slate-800 mb-2">Complaint Registered!</h2>
        <p className="text-slate-600 mb-6">Your unique Case ID is:</p>
        <div className="bg-slate-100 p-4 rounded-lg text-2xl font-mono text-slate-800 tracking-wider font-bold mb-6">
          {successId}
        </div>
        <p className="text-sm text-slate-500">
          The AI engine is structuring your complaint. Use the Tracker to view its progress.
        </p>
        <button 
          onClick={() => {setSuccessId(null); setFormData({...formData, subject: '', description: ''}); setAudioFile(null);}}
          className="mt-8 px-6 py-2 bg-blue-900 text-white rounded-lg hover:bg-blue-800 transition"
        >
          Submit Another
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto mt-8 bg-white rounded-xl shadow-sm overflow-hidden">
      <div className="bg-blue-900 p-6 text-white">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <Shield className="w-6 h-6" />
          Lodge New Complaint
        </h2>
        <p className="text-blue-200 mt-1 text-sm">Please provide accurate details. AI will assist in drafting the formal report.</p>
      </div>
      
      <form onSubmit={handleSubmit} className="p-6 space-y-5">
        {error && (
          <div className="p-4 bg-red-50 text-red-700 rounded-lg flex items-start gap-3 text-sm">
            <AlertCircle className="w-5 h-5 shrink-0" />
            <p>{error}</p>
          </div>
        )}
        
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Full Name *</label>
            <input type="text" value={formData.username} onChange={e => setFormData({...formData, username: e.target.value})} className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-900 focus:outline-none" placeholder="John Doe" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Phone Number *</label>
            <input type="text" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-900 focus:outline-none" placeholder="9876543210" />
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Incident Subject *</label>
          <input type="text" value={formData.subject} onChange={e => setFormData({...formData, subject: e.target.value})} className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-900 focus:outline-none" placeholder="Brief summary" />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Category</label>
          <select value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})} className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-900 focus:outline-none bg-white">
            <option>Cyber Fraud</option>
            <option>Theft</option>
            <option>Assault</option>
            <option>Women Safety</option>
            <option>Other</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Detailed Description</label>
          <textarea value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-900 focus:outline-none h-32" placeholder="What happened? (Optional if submitting voice)"></textarea>
        </div>
        
        <div className="border-2 border-dashed border-slate-300 rounded-xl p-6 text-center hover:bg-slate-50 transition cursor-pointer relative">
          <input type="file" accept=".wav,.mp3,.m4a" onChange={e => setAudioFile(e.target.files[0])} className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
          <div className="flex flex-col items-center gap-2">
            <FileAudio className="w-8 h-8 text-blue-600" />
            <p className="text-sm font-medium text-slate-700">Upload Voice Recording</p>
            <p className="text-xs text-slate-500">{audioFile ? audioFile.name : 'Supports .wav, .mp3, .m4a'}</p>
          </div>
        </div>
        
        <button disabled={loading} type="submit" className="w-full bg-blue-900 text-white font-semibold py-3 rounded-xl hover:bg-blue-800 transition disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-2">
          {loading ? (
            <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div> Processing...</>
          ) : (
            <><Upload className="w-5 h-5" /> Submit Report</>
          )}
        </button>
      </form>
    </div>
  );
}
