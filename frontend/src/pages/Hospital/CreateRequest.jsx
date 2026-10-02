import React, { useState } from 'react';
import { hospitalAPI } from '../../services/api';
import { useNavigate } from 'react-router-dom';

export const CreateRequest = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    patient_reference: 'PT1040',
    blood_group: 'O-',
    units_required: 3,
    priority: 'CRITICAL',
    required_date: new Date().toISOString().split('T')[0] + ' 11:30 PM',
    location: 'Peelamedu, Coimbatore',
    contact_dept: 'Emergency Department (+91 98765 43211)'
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await hospitalAPI.createRequest(formData);
      navigate('/hospital/manage-requests');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to publish request.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '700px' }}>
      <h2 style={{ marginBottom: '8px' }}>➕ Create Emergency Blood Request</h2>
      <p style={{ color: '#64748B', marginBottom: '20px' }}>Publish a new requirement directly onto the Live Emergency Board.</p>

      {error && (
        <div style={{ padding: '12px', backgroundColor: '#FEF2F2', border: '1px solid #FCA5A5', color: '#991B1B', borderRadius: '8px', marginBottom: '16px' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ backgroundColor: '#FFFFFF', padding: '24px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Patient Reference Code *</label>
            <input type="text" required value={formData.patient_reference} onChange={(e) => setFormData({ ...formData, patient_reference: e.target.value })} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
          </div>

          <div>
            <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Blood Group Required *</label>
            <select value={formData.blood_group} onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }}>
              {['O-', 'O+', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'].map(bg => <option key={bg} value={bg}>{bg}</option>)}
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Units Required *</label>
            <input type="number" min="1" max="20" required value={formData.units_required} onChange={(e) => setFormData({ ...formData, units_required: Number(e.target.value) })} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
          </div>

          <div>
            <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Priority Level *</label>
            <select value={formData.priority} onChange={(e) => setFormData({ ...formData, priority: e.target.value })} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }}>
              <option value="CRITICAL">🔴 CRITICAL</option>
              <option value="URGENT">🟠 URGENT</option>
              <option value="NORMAL">🟢 NORMAL</option>
            </select>
          </div>

          <div>
            <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Required By (Date & Time) *</label>
            <input type="text" required value={formData.required_date} onChange={(e) => setFormData({ ...formData, required_date: e.target.value })} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
          </div>

          <div>
            <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Hospital Location *</label>
            <input type="text" required value={formData.location} onChange={(e) => setFormData({ ...formData, location: e.target.value })} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
          </div>
        </div>

        <div style={{ marginTop: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Contact Department *</label>
          <input type="text" required value={formData.contact_dept} onChange={(e) => setFormData({ ...formData, contact_dept: e.target.value })} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <button type="submit" disabled={submitting} style={{ width: '100%', marginTop: '20px', backgroundColor: '#DC2626', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', fontWeight: 700, cursor: 'pointer' }}>
          {submitting ? 'Publishing...' : '🚨 Publish Emergency Request'}
        </button>
      </form>
    </div>
  );
};
