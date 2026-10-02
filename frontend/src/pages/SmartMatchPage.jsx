import React, { useState } from 'react';
import { matchingAPI } from '../services/api';
import { Heart, Search, CheckCircle } from 'lucide-react';

export const SmartMatchPage = () => {
  const [bloodGroup, setBloodGroup] = useState('O-');
  const [city, setCity] = useState('Coimbatore');
  const [area, setArea] = useState('Peelamedu');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await matchingAPI.findDonors(bloodGroup, city, area);
      setResults(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '24px' }}>
      <div style={{
        background: 'linear-gradient(135deg, #4338CA 0%, #312E81 100%)',
        color: 'white',
        padding: '30px',
        borderRadius: '16px',
        marginBottom: '25px'
      }}>
        <h1 style={{ margin: 0, fontSize: '2.2rem', fontWeight: 800 }}>🧠 SMART MATCHING ENGINE</h1>
        <p style={{ margin: '6px 0 0 0', color: '#E0E7FF' }}>
          Explainable rule-based algorithm evaluating blood compatibility, eligibility, location proximity & availability.
        </p>
      </div>

      <form onSubmit={handleSearch} style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0', display: 'flex', gap: '16px', alignItems: 'flex-end', marginBottom: '24px' }}>
        <div style={{ flex: 1 }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Target Blood Group *</label>
          <select value={bloodGroup} onChange={(e) => setBloodGroup(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1' }}>
            {['O-', 'O+', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'].map(bg => <option key={bg} value={bg}>{bg}</option>)}
          </select>
        </div>

        <div style={{ flex: 1 }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>City *</label>
          <input type="text" value={city} onChange={(e) => setCity(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1' }} />
        </div>

        <div style={{ flex: 1 }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Area / Locality</label>
          <input type="text" value={area} onChange={(e) => setArea(e.target.value)} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1' }} />
        </div>

        <button type="submit" disabled={loading} style={{ backgroundColor: '#4338CA', color: 'white', border: 'none', padding: '10px 20px', borderRadius: '6px', fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Search size={18} /> {loading ? 'Searching...' : 'Run Smart Match'}
        </button>
      </form>

      {results && (
        <div>
          <div style={{ backgroundColor: '#EFF6FF', border: '1px solid #BFDBFE', padding: '14px', borderRadius: '8px', marginBottom: '20px', color: '#1E40AF' }}>
            🩸 Compatible Donor Blood Groups for <strong>{bloodGroup}</strong>: <strong>{results.compatible_donor_groups.join(', ')}</strong>
          </div>

          <h3 style={{ marginBottom: '16px' }}>🎯 Ranked Suitable Donors ({results.matched_donors.length})</h3>

          {results.matched_donors.length === 0 ? (
            <p style={{ color: '#64748B' }}>No compatible & eligible donors found matching this criteria.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {results.matched_donors.map((d, idx) => (
                <div key={d.id} style={{ backgroundColor: '#FFFFFF', border: '1px solid #E2E8F0', padding: '18px', borderRadius: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h4 style={{ margin: 0, fontSize: '1.1rem' }}>
                      {idx + 1}. 👤 {d.name} (<span style={{ color: '#DC2626' }}>🩸 {d.blood_group}</span>)
                    </h4>
                    <span style={{ backgroundColor: '#DCFCE7', color: '#15803D', padding: '4px 10px', borderRadius: '6px', fontWeight: 800 }}>
                      🎯 {d.match_score}% Match
                    </span>
                  </div>
                  <p style={{ margin: '6px 0 0 0', color: '#475569', fontSize: '0.9rem' }}>
                    📍 Location: {d.area}, {d.city} | 📞 Phone: {d.phone} | Last Donation: {d.last_donation || 'Never'}
                  </p>
                  <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                    <span style={{ backgroundColor: '#F1F5F9', color: '#334155', fontSize: '0.75rem', fontWeight: 700, padding: '2px 8px', borderRadius: '4px' }}>
                      ✓ {d.match_details?.bg_desc}
                    </span>
                    <span style={{ backgroundColor: '#F1F5F9', color: '#334155', fontSize: '0.75rem', fontWeight: 700, padding: '2px 8px', borderRadius: '4px' }}>
                      ✓ {d.match_details?.loc_desc}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
