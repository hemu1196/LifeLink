import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AlertCircle } from 'lucide-react';

export const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [role, setRole] = useState('donor');
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    blood_group: 'O+',
    phone: '',
    city: 'Coimbatore',
    area: 'Peelamedu',
    license_number: '',
    hospital_type: 'Multispecialty',
    address: '',
    contact_person: '',
    emergency_contact: ''
  });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const payload = { ...formData, role };
      const res = await register(payload);
      if (res.role === 'donor') navigate('/donor/dashboard');
      else if (res.role === 'hospital') navigate('/hospital/dashboard');
      else if (res.role === 'blood_bank') navigate('/blood-bank/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '700px', margin: '30px auto', padding: '0 20px' }}>
      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
        <h1 style={{ color: '#DC2626', fontSize: '2.2rem', margin: 0, fontWeight: 800 }}>📝 Join LifeLink</h1>
        <p style={{ color: '#64748B', margin: '4px 0 0 0' }}>Create an Account to Start Coordinating Emergency Blood Support</p>
      </div>

      <div style={{ backgroundColor: '#FFFFFF', padding: '28px', borderRadius: '14px', border: '1px solid #E2E8F0' }}>
        <div style={{ marginBottom: '20px' }}>
          <label style={{ fontWeight: 600, fontSize: '0.9rem', display: 'block', marginBottom: '8px' }}>I am registering as a:</label>
          <div style={{ display: 'flex', gap: '10px' }}>
            {['donor', 'hospital', 'blood_bank'].map((r) => (
              <button
                key={r}
                type="button"
                onClick={() => setRole(r)}
                style={{
                  flex: 1,
                  padding: '10px',
                  borderRadius: '8px',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  cursor: 'pointer',
                  border: role === r ? '2px solid #DC2626' : '1px solid #CBD5E1',
                  backgroundColor: role === r ? '#FEF2F2' : '#FFFFFF',
                  color: role === r ? '#DC2626' : '#475569',
                  textTransform: 'capitalize'
                }}
              >
                {r === 'blood_bank' ? 'Blood Bank' : r}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
            <div>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Email Address *</label>
              <input type="email" name="email" required value={formData.email} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
            </div>

            <div>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Password *</label>
              <input type="password" name="password" required value={formData.password} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
            </div>

            <div>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Name / Organization Name *</label>
              <input type="text" name="name" required value={formData.name} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
            </div>

            <div>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Phone Number *</label>
              <input type="text" name="phone" required value={formData.phone} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
            </div>

            {role === 'donor' && (
              <div>
                <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Blood Group *</label>
                <select name="blood_group" value={formData.blood_group} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }}>
                  {['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].map(bg => <option key={bg} value={bg}>{bg}</option>)}
                </select>
              </div>
            )}

            {(role === 'hospital' || role === 'blood_bank') && (
              <div>
                <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>License Number *</label>
                <input type="text" name="license_number" required value={formData.license_number} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
              </div>
            )}

            <div>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>City *</label>
              <input type="text" name="city" required value={formData.city} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
            </div>

            <div>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.85rem', marginBottom: '4px' }}>Area / Locality</label>
              <input type="text" name="area" value={formData.area} onChange={handleChange} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
            </div>
          </div>

          {error && (
            <div style={{ marginTop: '16px', padding: '10px', backgroundColor: '#FEF2F2', border: '1px solid #FCA5A5', color: '#991B1B', borderRadius: '8px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <AlertCircle size={16} /> {error}
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            style={{ width: '100%', backgroundColor: '#DC2626', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', fontWeight: 700, cursor: 'pointer', marginTop: '20px' }}
          >
            {submitting ? 'Creating Account...' : 'Register Account'}
          </button>
        </form>

        <p style={{ textAlign: 'center', margin: '16px 0 0 0', fontSize: '0.9rem', color: '#64748B' }}>
          Already have an account? <Link to="/login" style={{ color: '#DC2626', fontWeight: 700, textDecoration: 'none' }}>Sign In</Link>
        </p>
      </div>
    </div>
  );
};
