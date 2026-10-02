import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { donorAPI } from '../services/api';
import { AlertCircle, Clock, MapPin, Phone, Heart, CheckCircle2 } from 'lucide-react';

export const EmergencyCard = ({ request, onResponded }) => {
  const { user } = useAuth();
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleDonate = async () => {
    if (!user) {
      setError('Please sign in as a Donor to respond to emergency requests.');
      return;
    }
    if (user.role !== 'donor') {
      setError('Only registered Donors can respond to blood requirements.');
      return;
    }

    setSubmitting(true);
    setError(null);
    setMessage(null);

    try {
      const res = await donorAPI.respond(request.id);
      setMessage(`🎉 Response Submitted! ${request.hospital_name} has received your donation request for Ref ${request.patient_reference}.`);
      if (onResponded) onResponded();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit response.');
    } finally {
      setSubmitting(false);
    }
  };

  const priorityColor = request.priority === 'CRITICAL' ? '#DC2626' : request.priority === 'URGENT' ? '#EA580C' : '#16A34A';
  const priorityBg = request.priority === 'CRITICAL' ? '#FEF2F2' : request.priority === 'URGENT' ? '#FFF7ED' : '#F0FDF4';

  return (
    <div style={{
      backgroundColor: '#FFFFFF',
      borderLeft: `5px solid ${priorityColor}`,
      border: '1px solid #E2E8F0',
      borderLeftWidth: '5px',
      borderRadius: '12px',
      padding: '20px',
      marginBottom: '16px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.03)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <div style={{
            backgroundColor: '#FEF2F2',
            border: '1px solid #FCA5A5',
            borderRadius: '12px',
            padding: '12px 18px',
            textAlign: 'center'
          }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 800, color: '#991B1B' }}>REQUIRED</span>
            <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#DC2626', lineHeight: 1 }}>{request.blood_group}</div>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#475569' }}>💉 {request.units_required} Unit(s)</span>
          </div>

          <div>
            <h3 style={{ margin: 0, fontSize: '1.25rem', color: '#0F172A' }}>🏥 {request.hospital_name}</h3>
            <p style={{ margin: '4px 0 0 0', color: '#64748B', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <MapPin size={15} /> <strong>Location:</strong> {request.location}
            </p>
            <p style={{ margin: '4px 0 0 0', color: '#64748B', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Clock size={15} /> <strong>Required By:</strong> {request.required_date} | 🏷️ <strong>Ref:</strong> <code>{request.patient_reference}</code>
            </p>
          </div>
        </div>

        <div style={{ textAlign: 'right', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '8px' }}>
          <span style={{
            backgroundColor: priorityBg,
            color: priorityColor,
            border: `1px solid ${priorityColor}`,
            padding: '4px 12px',
            borderRadius: '9999px',
            fontSize: '0.75rem',
            fontWeight: 800,
            textTransform: 'uppercase'
          }}>
            ● {request.priority} PRIORITY
          </span>
          <div style={{ fontSize: '0.85rem', color: '#475569' }}>
            <Phone size={14} style={{ display: 'inline', marginRight: '4px' }} /> {request.contact_dept}
          </div>
          <button
            onClick={handleDonate}
            disabled={submitting}
            style={{
              backgroundColor: '#DC2626',
              color: '#FFFFFF',
              border: 'none',
              padding: '10px 18px',
              borderRadius: '8px',
              fontWeight: 700,
              cursor: submitting ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              marginTop: '4px'
            }}
          >
            <Heart size={16} fill="#FFFFFF" /> {submitting ? 'Submitting...' : 'I Can Donate'}
          </button>
        </div>
      </div>

      {message && (
        <div style={{ marginTop: '12px', padding: '10px 14px', backgroundColor: '#F0FDF4', border: '1px solid #86EFAC', borderRadius: '8px', color: '#166534', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={18} /> {message}
        </div>
      )}

      {error && (
        <div style={{ marginTop: '12px', padding: '10px 14px', backgroundColor: '#FEF2F2', border: '1px solid #FCA5A5', borderRadius: '8px', color: '#991B1B', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <AlertCircle size={18} /> {error}
        </div>
      )}
    </div>
  );
};
