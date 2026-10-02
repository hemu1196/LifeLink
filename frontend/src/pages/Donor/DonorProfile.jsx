import React, { useState, useEffect } from 'react';
import { donorAPI } from '../../services/api';
import { LoadingSpinner } from '../../components/LoadingSpinner';

export const DonorProfile = () => {
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({ name: '', phone: '', city: '', area: '', last_donation: '', availability: 'AVAILABLE' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    donorAPI.getProfile().then((res) => {
      setProfile(res.data);
      setFormData({
        name: res.data.name || '',
        phone: res.data.phone || '',
        city: res.data.city || '',
        area: res.data.area || '',
        last_donation: res.data.last_donation || '',
        availability: res.data.availability || 'AVAILABLE'
      });
      setLoading(false);
    });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    try {
      await donorAPI.updateProfile(formData);
      setMessage('Profile updated successfully!');
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div style={{ maxWidth: '600px' }}>
      <h2 style={{ marginBottom: '20px' }}>👤 Manage Profile & Availability</h2>

      {message && (
        <div style={{ padding: '12px', backgroundColor: '#F0FDF4', border: '1px solid #86EFAC', borderRadius: '8px', color: '#166534', marginBottom: '20px', fontWeight: 600 }}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ backgroundColor: '#FFFFFF', padding: '24px', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Full Name</label>
          <input type="text" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Blood Group (Immutable)</label>
          <input type="text" disabled value={profile?.blood_group} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', backgroundColor: '#F1F5F9', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Phone Number</label>
          <input type="text" value={formData.phone} onChange={(e) => setFormData({ ...formData, phone: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>City</label>
          <input type="text" value={formData.city} onChange={(e) => setFormData({ ...formData, city: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Area / Locality</label>
          <input type="text" value={formData.area} onChange={(e) => setFormData({ ...formData, area: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Last Donation Date (YYYY-MM-DD)</label>
          <input type="date" value={formData.last_donation} onChange={(e) => setFormData({ ...formData, last_donation: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Donation Availability Status</label>
          <select value={formData.availability} onChange={(e) => setFormData({ ...formData, availability: e.target.value })} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }}>
            <option value="AVAILABLE">AVAILABLE</option>
            <option value="UNAVAILABLE">UNAVAILABLE</option>
          </select>
        </div>

        <button type="submit" disabled={saving} style={{ backgroundColor: '#DC2626', color: 'white', border: 'none', padding: '12px 20px', borderRadius: '8px', fontWeight: 700, cursor: 'pointer' }}>
          {saving ? 'Saving...' : 'Update Profile'}
        </button>
      </form>
    </div>
  );
};
