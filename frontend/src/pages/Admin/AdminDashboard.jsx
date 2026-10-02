import React, { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminAPI.getStats().then((res) => {
      setStats(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>🛡️ System Governance Dashboard</h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '30px' }}>
        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Total Donors</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#0F172A', marginTop: '4px' }}>{stats?.total_donors}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Verified Hospitals</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#16A34A', marginTop: '4px' }}>{stats?.verified_hospitals}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0', borderLeft: '4px solid #EA580C' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Pending Verifications</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#EA580C', marginTop: '4px' }}>{stats?.pending_hospitals}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Total Blood Stock</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#DC2626', marginTop: '4px' }}>{stats?.total_blood_units} Units</div>
        </div>
      </div>
    </div>
  );
};
