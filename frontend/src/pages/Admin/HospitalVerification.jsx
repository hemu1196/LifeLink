import React, { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const HospitalVerification = () => {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHospitals = async () => {
    try {
      const res = await adminAPI.getHospitals();
      setHospitals(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHospitals();
  }, []);

  const handleVerify = async (id, status) => {
    try {
      await adminAPI.verifyHospital(id, status);
      fetchHospitals();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <LoadingSpinner />;

  const pending = hospitals.filter(h => h.verification_status === 'PENDING');
  const verified = hospitals.filter(h => h.verification_status === 'VERIFIED');

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>🏥 Hospital Verification & Licensing Desk</h2>

      {pending.length > 0 && (
        <div style={{ marginBottom: '30px' }}>
          <h3 style={{ color: '#EA580C', marginBottom: '14px' }}>⏳ Pending Verification Applications ({pending.length})</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {pending.map((h) => (
              <div key={h.id} style={{ backgroundColor: '#FFF7ED', border: '1px solid #FDBA74', padding: '18px', borderRadius: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h4 style={{ margin: 0, fontSize: '1.1rem' }}>🏥 {h.hospital_name} (License: <code>{h.license_number}</code>)</h4>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button onClick={() => handleVerify(h.id, 'VERIFIED')} style={{ backgroundColor: '#16A34A', color: 'white', border: 'none', padding: '8px 14px', borderRadius: '6px', fontWeight: 600, cursor: 'pointer' }}>
                      Approve Hospital
                    </button>
                    <button onClick={() => handleVerify(h.id, 'REJECTED')} style={{ backgroundColor: '#DC2626', color: 'white', border: 'none', padding: '8px 14px', borderRadius: '6px', fontWeight: 600, cursor: 'pointer' }}>
                      Reject
                    </button>
                  </div>
                </div>
                <p style={{ margin: '8px 0 0 0', color: '#475569', fontSize: '0.9rem' }}>
                  City: {h.city} | Contact Person: {h.contact_person} ({h.phone}) | Type: {h.hospital_type}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      <h3>✅ Verified Hospitals Network</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#FFFFFF', borderRadius: '12px', overflow: 'hidden', border: '1px solid #E2E8F0' }}>
        <thead>
          <tr style={{ backgroundColor: '#F8FAFC', textTransform: 'uppercase', fontSize: '0.8rem', color: '#64748B' }}>
            <th style={{ padding: '14px', textAlign: 'left' }}>Hospital Name</th>
            <th style={{ padding: '14px', textAlign: 'left' }}>License Number</th>
            <th style={{ padding: '14px', textAlign: 'left' }}>City</th>
            <th style={{ padding: '14px', textAlign: 'left' }}>Phone</th>
            <th style={{ padding: '14px', textAlign: 'left' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {verified.map((h) => (
            <tr key={h.id} style={{ borderBottom: '1px solid #E2E8F0' }}>
              <td style={{ padding: '14px', fontWeight: 600 }}>{h.hospital_name}</td>
              <td style={{ padding: '14px' }}><code>{h.license_number}</code></td>
              <td style={{ padding: '14px' }}>{h.city}</td>
              <td style={{ padding: '14px' }}>{h.phone}</td>
              <td style={{ padding: '14px' }}>
                <span style={{ backgroundColor: '#DBEAFE', color: '#1E40AF', padding: '3px 8px', borderRadius: '4px', fontWeight: 700, fontSize: '0.85rem' }}>
                  VERIFIED
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
