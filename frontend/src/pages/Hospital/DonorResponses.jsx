import React, { useState, useEffect } from 'react';
import { hospitalAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const DonorResponses = () => {
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchResponses = async () => {
    try {
      const res = await hospitalAPI.getDonorResponses();
      setResponses(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResponses();
  }, []);

  const handleUpdateStatus = async (id, status) => {
    try {
      await hospitalAPI.updateResponseStatus(id, status);
      fetchResponses();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>👥 Donor Emergency Responses</h2>

      {responses.length === 0 ? (
        <div style={{ backgroundColor: '#FFFFFF', padding: '30px', textAlign: 'center', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <p style={{ color: '#64748B', margin: 0 }}>No donor responses received yet.</p>
        </div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#FFFFFF', borderRadius: '12px', overflow: 'hidden', border: '1px solid #E2E8F0' }}>
          <thead>
            <tr style={{ backgroundColor: '#F8FAFC', textTransform: 'uppercase', fontSize: '0.8rem', color: '#64748B' }}>
              <th style={{ padding: '14px', textAlign: 'left' }}>Ref Code</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Donor Name</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Blood Group</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Phone</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Status</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {responses.map((resp) => (
              <tr key={resp.id} style={{ borderBottom: '1px solid #E2E8F0' }}>
                <td style={{ padding: '14px' }}><code>{resp.patient_reference}</code></td>
                <td style={{ padding: '14px', fontWeight: 600 }}>{resp.donor_name}</td>
                <td style={{ padding: '14px', fontWeight: 800, color: '#DC2626' }}>🩸 {resp.blood_group}</td>
                <td style={{ padding: '14px' }}>{resp.phone}</td>
                <td style={{ padding: '14px' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.85rem', color: resp.status === 'ACCEPTED' || resp.status === 'COMPLETED' ? '#16A34A' : '#EA580C' }}>
                    {resp.status}
                  </span>
                </td>
                <td style={{ padding: '14px' }}>
                  <div style={{ display: 'flex', gap: '6px' }}>
                    <button onClick={() => handleUpdateStatus(resp.id, 'ACCEPTED')} style={{ backgroundColor: '#2563EB', color: 'white', border: 'none', padding: '6px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer' }}>
                      Accept
                    </button>
                    <button onClick={() => handleUpdateStatus(resp.id, 'COMPLETED')} style={{ backgroundColor: '#16A34A', color: 'white', border: 'none', padding: '6px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer' }}>
                      Complete
                    </button>
                    <button onClick={() => handleUpdateStatus(resp.id, 'DECLINED')} style={{ backgroundColor: '#64748B', color: 'white', border: 'none', padding: '6px 10px', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 600, cursor: 'pointer' }}>
                      Decline
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
