import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { User, Building2, Droplet, Shield, KeyRound, AlertCircle } from 'lucide-react';

export const Login = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [role, setRole] = useState('donor');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await login(email, password, role);
      if (res.role === 'donor') navigate('/donor/dashboard');
      else if (res.role === 'hospital') navigate('/hospital/dashboard');
      else if (res.role === 'blood_bank') navigate('/blood-bank/dashboard');
      else if (res.role === 'admin') navigate('/admin/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please check credentials.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDemoLogin = async (demoEmail, demoPassword, demoRole) => {
    setError(null);
    setSubmitting(true);
    try {
      const res = await login(demoEmail, demoPassword, demoRole);
      if (res.role === 'donor') navigate('/donor/dashboard');
      else if (res.role === 'hospital') navigate('/hospital/dashboard');
      else if (res.role === 'blood_bank') navigate('/blood-bank/dashboard');
      else if (res.role === 'admin') navigate('/admin/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Demo login failed.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '40px auto', padding: '0 20px' }}>
      <div style={{ textAlignment: 'center', textAlign: 'center', marginBottom: '30px' }}>
        <h1 style={{ color: '#DC2626', fontSize: '2.4rem', margin: 0, fontWeight: 800 }}>🩸 Sign In to LifeLink</h1>
        <p style={{ color: '#64748B', margin: '6px 0 0 0' }}>Connecting Donors • Hospitals • Blood Banks in Real-Time</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '30px', alignItems: 'start' }}>
        {/* Main Login Form */}
        <div style={{ backgroundColor: '#FFFFFF', padding: '28px', borderRadius: '14px', border: '1px solid #E2E8F0', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
            {[
              { id: 'donor', label: 'Donor', icon: User },
              { id: 'hospital', label: 'Hospital', icon: Building2 },
              { id: 'blood_bank', label: 'Blood Bank', icon: Droplet },
              { id: 'admin', label: 'Admin', icon: Shield },
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setRole(tab.id)}
                  style={{
                    flex: 1,
                    padding: '8px 4px',
                    borderRadius: '8px',
                    fontWeight: 600,
                    fontSize: '0.8rem',
                    cursor: 'pointer',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '4px',
                    border: role === tab.id ? '2px solid #DC2626' : '1px solid #CBD5E1',
                    backgroundColor: role === tab.id ? '#FEF2F2' : '#FFFFFF',
                    color: role === tab.id ? '#DC2626' : '#64748B'
                  }}
                >
                  <Icon size={16} />
                  {tab.label}
                </button>
              );
            })}
          </div>

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.9rem', marginBottom: '6px', color: '#334155' }}>Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                style={{ width: '100%', padding: '10px 12px', borderRadius: '8px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }}
              />
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ display: 'block', fontWeight: 600, fontSize: '0.9rem', marginBottom: '6px', color: '#334155' }}>Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                style={{ width: '100%', padding: '10px 12px', borderRadius: '8px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }}
              />
            </div>

            {error && (
              <div style={{ padding: '10px', backgroundColor: '#FEF2F2', border: '1px solid #FCA5A5', color: '#991B1B', borderRadius: '8px', marginBottom: '16px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <AlertCircle size={16} /> {error}
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              style={{ width: '100%', backgroundColor: '#DC2626', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', fontWeight: 700, cursor: 'pointer', fontSize: '1rem' }}
            >
              {submitting ? 'Authenticating...' : `Sign In as ${role.toUpperCase()}`}
            </button>
          </form>

          <p style={{ textAlign: 'center', margin: '18px 0 0 0', fontSize: '0.9rem', color: '#64748B' }}>
            Don't have an account? <Link to="/register" style={{ color: '#DC2626', fontWeight: 700, textDecoration: 'none' }}>Register Now</Link>
          </p>
        </div>

        {/* Quick Demo One-Click Login Box */}
        <div style={{ backgroundColor: '#EFF6FF', padding: '24px', borderRadius: '14px', border: '1px solid #BFDBFE' }}>
          <h3 style={{ margin: '0 0 8px 0', color: '#1E40AF', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <KeyRound size={20} /> One-Click Quick Demo Login
          </h3>
          <p style={{ color: '#3B82F6', fontSize: '0.85rem', margin: '0 0 16px 0' }}>Click any button below to immediately log in with preset test accounts:</p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <button
              onClick={() => handleDemoLogin('rahul@gmail.com', 'donor123', 'donor')}
              style={{ backgroundColor: '#FFFFFF', border: '1px solid #93C5FD', padding: '10px 14px', borderRadius: '8px', fontWeight: 600, color: '#1E3A8A', textAlign: 'left', cursor: 'pointer' }}
            >
              👤 Donor: Rahul Verma (O-)
            </button>
            <button
              onClick={() => handleDemoLogin('cityhospital@gmail.com', 'hospital123', 'hospital')}
              style={{ backgroundColor: '#FFFFFF', border: '1px solid #93C5FD', padding: '10px 14px', borderRadius: '8px', fontWeight: 600, color: '#1E3A8A', textAlign: 'left', cursor: 'pointer' }}
            >
              🏥 Hospital: City Hospital
            </button>
            <button
              onClick={() => handleDemoLogin('cbebloodbank@gmail.com', 'bloodbank123', 'blood_bank')}
              style={{ backgroundColor: '#FFFFFF', border: '1px solid #93C5FD', padding: '10px 14px', borderRadius: '8px', fontWeight: 600, color: '#1E3A8A', textAlign: 'left', cursor: 'pointer' }}
            >
              🩸 Blood Bank: Central BB
            </button>
            <button
              onClick={() => handleDemoLogin('admin@lifelink.com', 'admin123', 'admin')}
              style={{ backgroundColor: '#FFFFFF', border: '1px solid #93C5FD', padding: '10px 14px', borderRadius: '8px', fontWeight: 600, color: '#1E3A8A', textAlign: 'left', cursor: 'pointer' }}
            >
              🛡️ Admin: System Administrator
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
