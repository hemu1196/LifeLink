import React, { useState, useEffect } from 'react';
import { donorAPI, emergencyBoardAPI } from '../../services/api';
import { EmergencyCard } from '../../components/EmergencyCard';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const DonorDashboard = () => {
  const [profile, setProfile] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [profRes, eligRes, reqRes] = await Promise.all([
          donorAPI.getProfile(),
          donorAPI.getEligibility(),
          emergencyBoardAPI.getBoard('ALL')
        ]);
        setProfile(profRes.data);
        setEligibility(eligRes.data);
        setRequests(reqRes.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h2 style={{ margin: '0 0 20px 0', fontSize: '1.8rem', color: '#0F172A' }}>
        Welcome back, <strong>{profile?.name}</strong>! 👋
      </h2>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '30px' }}>
        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Blood Group</div>
          <div style={{ fontSize: '2rem', fontWeight: 800, color: '#DC2626', marginTop: '4px' }}>🩸 {profile?.blood_group}</div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Status</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 700, color: eligibility?.eligible ? '#16A34A' : '#DC2626', marginTop: '8px' }}>
            {eligibility?.eligible ? '🟢 Eligible' : '🔴 Ineligible'}
          </div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Last Donation</div>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#0F172A', marginTop: '8px' }}>
            {profile?.last_donation || 'None Logged'}
          </div>
        </div>

        <div style={{ backgroundColor: '#FFFFFF', padding: '18px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>Availability</div>
          <div style={{ fontSize: '1.1rem', fontWeight: 700, color: '#16A34A', marginTop: '8px' }}>
            {profile?.availability}
          </div>
        </div>
      </div>

      <h3 style={{ marginBottom: '16px', color: '#0F172A' }}>🚨 Live Emergency Requirements</h3>
      {requests.length === 0 ? (
        <p style={{ color: '#64748B' }}>No active requirements right now.</p>
      ) : (
        requests.slice(0, 4).map((req) => <EmergencyCard key={req.id} request={req} />)
      )}
    </div>
  );
};
