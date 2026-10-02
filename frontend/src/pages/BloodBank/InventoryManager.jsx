import React, { useState, useEffect } from 'react';
import { bloodBankAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const InventoryManager = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    bloodBankAPI.getInventory().then((res) => {
      setItems(res.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>📋 Batch Inventory Records</h2>

      {items.length === 0 ? (
        <div style={{ backgroundColor: '#FFFFFF', padding: '30px', textAlign: 'center', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <p style={{ color: '#64748B', margin: 0 }}>No blood inventory batches logged.</p>
        </div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#FFFFFF', borderRadius: '12px', overflow: 'hidden', border: '1px solid #E2E8F0' }}>
          <thead>
            <tr style={{ backgroundColor: '#F8FAFC', textTransform: 'uppercase', fontSize: '0.8rem', color: '#64748B' }}>
              <th style={{ padding: '14px', textAlign: 'left' }}>Batch ID</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Blood Group</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Units</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Collection Date</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Expiry Date</th>
              <th style={{ padding: '14px', textAlign: 'left' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} style={{ borderBottom: '1px solid #E2E8F0' }}>
                <td style={{ padding: '14px' }}>BATCH-{item.id}</td>
                <td style={{ padding: '14px', fontWeight: 800, color: '#DC2626' }}>🩸 {item.blood_group}</td>
                <td style={{ padding: '14px', fontWeight: 700 }}>{item.units} Unit(s)</td>
                <td style={{ padding: '14px' }}>{item.collection_date}</td>
                <td style={{ padding: '14px' }}>{item.expiry_date}</td>
                <td style={{ padding: '14px' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.85rem', color: '#16A34A', backgroundColor: '#F0FDF4', padding: '3px 8px', borderRadius: '4px' }}>
                    {item.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
