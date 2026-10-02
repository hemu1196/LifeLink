import React, { useState, useEffect } from 'react';
import { bloodBankAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const BloodBankDashboard = () => {
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    bloodBankAPI.getSummary().then((res) => {
      setSummary(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  const allGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
  const stockMap = {};
  summary.forEach((item) => { stockMap[item.blood_group] = item.total_units; });

  const totalUnits = summary.reduce((acc, curr) => acc + curr.total_units, 0);

  return (
    <div>
      <h2 style={{ marginBottom: '8px' }}>🩸 Blood Bank Inventory Overview</h2>
      <p style={{ color: '#64748B', marginBottom: '24px' }}>Total Network Available Stock: <strong>{totalUnits} Units</strong></p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        {allGroups.map((bg) => {
          const units = stockMap[bg] || 0;
          const isLow = units < 3;
          return (
            <div key={bg} style={{ backgroundColor: '#FFFFFF', padding: '20px', borderRadius: '12px', border: isLow ? '2px solid #DC2626' : '1px solid #E2E8F0', textAlign: 'center' }}>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#DC2626' }}>{bg}</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#0F172A', margin: '6px 0' }}>{units} Units</div>
              <span style={{ fontSize: '0.75rem', fontWeight: 800, padding: '3px 8px', borderRadius: '9999px', backgroundColor: isLow ? '#FEF2F2' : '#F0FDF4', color: isLow ? '#991B1B' : '#166534' }}>
                {isLow ? '⚠️ LOW STOCK' : 'NORMAL'}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
