import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';
import { LoadingSpinner } from '../components/LoadingSpinner';

export const AnalyticsPage = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    analyticsAPI.getSummary().then((res) => {
      setData(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  const kpis = data?.kpis || {};
  const inv = data?.inventory_distribution || [];

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '24px' }}>
      <div style={{
        background: 'linear-gradient(135deg, #0284C7 0%, #0369A1 100%)',
        color: 'white',
        padding: '30px',
        borderRadius: '16px',
        marginBottom: '25px'
      }}>
        <h1 style={{ margin: 0, fontSize: '2.2rem', fontWeight: 800 }}>📊 ANALYTICS & SYSTEM INSIGHTS</h1>
        <p style={{ margin: '6px 0 0 0', color: '#E0F2FE' }}>
          Real-time telemetry, blood availability trends, emergency response metrics & donation analytics.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '30px' }}>
        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Registered Donors</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#0F172A', marginTop: '4px' }}>{kpis.total_donors}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Available Blood Stock</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#DC2626', marginTop: '4px' }}>{kpis.total_inventory_units} Units</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Active Requirements</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#EA580C', marginTop: '4px' }}>{kpis.active_requests}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Fulfilled Requirements</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#16A34A', marginTop: '4px' }}>{kpis.fulfilled_requests}</div>
        </div>
      </div>

      <div style={{ backgroundColor: '#FFFFFF', padding: '24px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
        <h3 style={{ margin: '0 0 16px 0' }}>🩸 Blood Group Stock Inventory Distribution</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
          {inv.map((item) => (
            <div key={item.blood_group} style={{ backgroundColor: '#F8FAFC', padding: '14px', borderRadius: '8px', border: '1px solid #E2E8F0', textAlign: 'center' }}>
              <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#DC2626' }}>{item.blood_group}</div>
              <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#0F172A' }}>{item.total_units} Units</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
