import React, { useState, useEffect } from 'react';
import { donorAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const DonationHistory = () => {
  const [donations, setDonations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    donorAPI.getDonations().then((res) => {
      setDonations(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>📜 Donation History & Records</h2>

      {donations.length === 0 ? (
        <div style={{ backgroundColor: '#FFFFFF', padding: '30px', textAlign: 'center', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <p style={{ color: '#64748B', margin: 0 }}>No past donation records logged.</p>
        </div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#FFFFFF', borderRadius: '12px', overflow: 'hidden', border: '1px solid #E2E8F0' }}>
          <thead>
            <tr style={{ backgroundColor: '#F8FAFC', textTransform: 'uppercase', fontSize: '0.8rem', color: '#64748B' }}>
              <th style={{ padding: '14px', textAlign: 'left' }}>Donation ID</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Date</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Units Donated</th>
            </tr>
          </thead>
          <tbody>
            {donations.map((d) => (
              <tr key={d.id} style={{ borderBottom: '1px solid #E2E8F0' }}>
                <td style={{ padding: '14px' }}>DON-{d.id}</td>
                <td style={{ padding: '14px' }}>{d.donation_date}</td>
                <td style={{ padding: '14px', fontWeight: 700, color: '#DC2626' }}>🩸 {d.units} Unit(s)</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
