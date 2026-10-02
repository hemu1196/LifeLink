import React, { useState, useEffect } from 'react';
import { emergencyBoardAPI } from '../services/api';
import { EmergencyCard } from '../components/EmergencyCard';
import { LoadingSpinner } from '../components/LoadingSpinner';

export const Home = () => {
  const [requests, setRequests] = useState([]);
  const [priority, setPriority] = useState('ALL');
  const [loading, setLoading] = useState(true);

  const fetchBoard = async () => {
    setLoading(true);
    try {
      const res = await emergencyBoardAPI.getBoard(priority);
      setRequests(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBoard();
  }, [priority]);

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '24px' }}>
      <div style={{
        background: 'linear-gradient(135deg, #DC2626 0%, #991B1B 100%)',
        color: 'white',
        padding: '30px',
        borderRadius: '16px',
        marginBottom: '25px',
        boxShadow: '0 10px 15px -3px rgba(220, 38, 38, 0.3)'
      }}>
        <h1 style={{ margin: 0, fontSize: '2.4rem', fontWeight: 800 }}>🚨 LIVE EMERGENCY BLOOD BOARD</h1>
        <p style={{ margin: '8px 0 0 0', fontSize: '1.1rem', color: '#FEE2E2' }}>
          Real-time emergency blood requirements published directly by verified hospitals.
        </p>
      </div>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        {['ALL', 'CRITICAL', 'URGENT', 'NORMAL'].map((p) => (
          <button
            key={p}
            onClick={() => setPriority(p)}
            style={{
              padding: '8px 18px',
              borderRadius: '8px',
              fontWeight: 700,
              fontSize: '0.85rem',
              cursor: 'pointer',
              border: priority === p ? '2px solid #DC2626' : '1px solid #CBD5E1',
              backgroundColor: priority === p ? '#FEF2F2' : '#FFFFFF',
              color: priority === p ? '#DC2626' : '#475569'
            }}
          >
            {p === 'CRITICAL' ? '🔴 Critical' : p === 'URGENT' ? '🟠 Urgent' : p === 'NORMAL' ? '🟢 Normal' : 'All Requirements'}
          </button>
        ))}
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : requests.length === 0 ? (
        <div style={{ backgroundColor: '#FFFFFF', padding: '40px', textAlign: 'center', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <h3>✨ No active emergency blood requirements at the moment.</h3>
        </div>
      ) : (
        <div>
          <p style={{ color: '#64748B', fontWeight: 600, marginBottom: '16px' }}>Showing {requests.length} active requirement(s):</p>
          {requests.map((req) => (
            <EmergencyCard key={req.id} request={req} onResponded={fetchBoard} />
          ))}
        </div>
      )}
    </div>
  );
};
