import React, { useState } from 'react';
import { bloodBankAPI } from '../../services/api';
import { useNavigate } from 'react-router-dom';

export const AddStock = () => {
  const navigate = useNavigate();
  const today = new Date().toISOString().split('T')[0];
  const nextMonth = new Date(Date.now() + 35 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  const [formData, setFormData] = useState({
    blood_group: 'O-',
    units: 5,
    collection_date: today,
    expiry_date: nextMonth
  });
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);
    try {
      await bloodBankAPI.addInventory(formData);
      setMessage(`Added ${formData.units} unit(s) of ${formData.blood_group} blood!`);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px' }}>
      <h2 style={{ marginBottom: '20px' }}>➕ Add New Blood Inventory Batch</h2>

      {message && (
        <div style={{ padding: '12px', backgroundColor: '#F0FDF4', border: '1px solid #86EFAC', borderRadius: '8px', color: '#166534', marginBottom: '16px', fontWeight: 600 }}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ backgroundColor: '#FFFFFF', padding: '24px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Blood Group *</label>
          <select value={formData.blood_group} onChange={(e) => setFormData({ ...formData, blood_group: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }}>
            {['O-', 'O+', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'].map(bg => <option key={bg} value={bg}>{bg}</option>)}
          </select>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Units Count *</label>
          <input type="number" min="1" max="100" required value={formData.units} onChange={(e) => setFormData({ ...formData, units: Number(e.target.value) })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Collection Date *</label>
          <input type="date" required value={formData.collection_date} onChange={(e) => setFormData({ ...formData, collection_date: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Expiry Date *</label>
          <input type="date" required value={formData.expiry_date} onChange={(e) => setFormData({ ...formData, expiry_date: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <button type="submit" disabled={submitting} style={{ width: '100%', backgroundColor: '#DC2626', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', fontWeight: 700, cursor: 'pointer' }}>
          {submitting ? 'Saving...' : 'Save Blood Batch'}
        </button>
      </form>
    </div>
  );
};
