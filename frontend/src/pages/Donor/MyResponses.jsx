import React, { useState, useEffect } from 'react';
import { donorAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const MyResponses = () => {
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    donorAPI.getResponses().then((res) => {
      setResponses(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>❤️ My Emergency Donation Responses</h2>

      {responses.length === 0 ? (
        <div style={{ backgroundColor: '#FFFFFF', padding: '30px', textAlign: 'center', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <p style={{ color: '#64748B', margin: 0 }}>You haven't responded to any emergency requirements yet.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {responses.map((resp) => {
            const statusColor = resp.status === 'ACCEPTED' || resp.status === 'COMPLETED' ? '#16A34A' : '#EA580C';
            return (
              <div key={resp.id} style={{ backgroundColor: '#FFFFFF', border: '1px solid #E2E8F0', padding: '18px', borderRadius: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h3 style={{ margin: 0, fontSize: '1.1rem' }}>🏥 {resp.hospital_name} (Ref: <code>{resp.patient_reference}</code>)</h3>
                  <span style={{ fontWeight: 800, color: statusColor, backgroundColor: '#F1F5F9', padding: '4px 10px', borderRadius: '6px', fontSize: '0.85rem' }}>
                    {resp.status}
                  </span>
                </div>
                <p style={{ margin: '8px 0 0 0', color: '#64748B', fontSize: '0.9rem' }}>
                  📍 Location: {resp.location} | ⏰ Required By: {resp.required_date}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
