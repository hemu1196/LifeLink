import React, { useState, useEffect } from 'react';
import { hospitalAPI, matchingAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const ManageRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchRequests = async () => {
    try {
      const res = await hospitalAPI.getRequests();
      setRequests(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRequests();
  }, []);

  const handleStatusChange = async (id, status) => {
    try {
      await hospitalAPI.updateRequestStatus(id, status);
      fetchRequests();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div>
      <h2 style={{ marginBottom: '20px' }}>🚨 Hospital Active Emergency Requests</h2>

      {requests.length === 0 ? (
        <div style={{ backgroundColor: '#FFFFFF', padding: '30px', textAlign: 'center', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <p style={{ color: '#64748B', margin: 0 }}>No blood requests found.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {requests.map((req) => (
            <div key={req.id} style={{ backgroundColor: '#FFFFFF', border: '1px solid #E2E8F0', padding: '20px', borderRadius: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3 style={{ margin: 0, fontSize: '1.2rem' }}>
                  Ref: <code>{req.patient_reference}</code> | Blood Needed: <span style={{ color: '#DC2626' }}>{req.blood_group}</span> ({req.units_required} Units)
                </h3>
                <span style={{ fontWeight: 800, padding: '4px 10px', borderRadius: '9999px', fontSize: '0.85rem', backgroundColor: req.status === 'ACTIVE' ? '#FEF2F2' : '#F1F5F9', color: req.status === 'ACTIVE' ? '#DC2626' : '#64748B' }}>
                  {req.priority} • {req.status}
                </span>
              </div>
              <p style={{ color: '#64748B', fontSize: '0.9rem', margin: '8px 0 12px 0' }}>
                Required By: {req.required_date} | Responded Donors: <strong>{req.response_count}</strong>
              </p>

              {req.status === 'ACTIVE' && (
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button onClick={() => handleStatusChange(req.id, 'FULFILLED')} style={{ backgroundColor: '#16A34A', color: 'white', border: 'none', padding: '8px 14px', borderRadius: '6px', fontWeight: 600, cursor: 'pointer' }}>
                    Mark FULFILLED
                  </button>
                  <button onClick={() => handleStatusChange(req.id, 'CANCELLED')} style={{ backgroundColor: '#64748B', color: 'white', border: 'none', padding: '8px 14px', borderRadius: '6px', fontWeight: 600, cursor: 'pointer' }}>
                    Cancel Request
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
