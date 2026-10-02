import React, { useState, useEffect } from 'react';
import { hospitalAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const HospitalDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    hospitalAPI.getDashboard().then((res) => {
      setData(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h2 style={{ margin: 0, fontSize: '1.8rem' }}>🏥 <strong>{data?.hospital_name}</strong> Dashboard</h2>
          <span style={{ fontSize: '0.85rem', color: '#64748B' }}>Status: <strong>{data?.verification_status}</strong></span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '30px' }}>
        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Active Requests</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#0F172A', marginTop: '4px' }}>{data?.active_requests_count}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0', borderLeft: '4px solid #DC2626' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Critical Requests</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#DC2626', marginTop: '4px' }}>{data?.critical_requests_count}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Donors Responded</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#2563EB', marginTop: '4px' }}>{data?.donors_responded_count}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Requests Fulfilled</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#16A34A', marginTop: '4px' }}>{data?.requests_fulfilled_count}</div>
        </div>
      </div>
    </div>
  );
};
