import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Heart, Activity, User, LogOut, Bell, Shield, Building2, Droplet } from 'lucide-react';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <nav style={{
      backgroundColor: '#FFFFFF',
      borderBottom: '1px solid #E2E8F0',
      padding: '12px 28px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      position: 'sticky',
      top: 0,
      zIndex: 50,
      boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
    }}>
      <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{ fontSize: '1.8rem', color: '#DC2626', fontWeight: 800 }}>🩸 LifeLink</span>
        <span style={{
          backgroundColor: '#FEF2F2',
          color: '#DC2626',
          fontSize: '0.75rem',
          fontWeight: 700,
          padding: '3px 8px',
          borderRadius: '9999px',
          border: '1px solid #FCA5A5'
        }}>
          LIVE V2.0
        </span>
      </Link>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <Link to="/" style={{ textDecoration: 'none', color: '#475569', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Activity size={18} color="#DC2626" /> Emergency Board
        </Link>
        <Link to="/smart-match" style={{ textDecoration: 'none', color: '#475569', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Heart size={18} color="#4338CA" /> Smart Match
        </Link>
        <Link to="/analytics" style={{ textDecoration: 'none', color: '#475569', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Activity size={18} color="#0284C7" /> Analytics
        </Link>
        <Link to="/notifications" style={{ textDecoration: 'none', color: '#475569', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Bell size={18} color="#059669" /> Notifications
        </Link>

        {user ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px', borderLeft: '1px solid #E2E8F0', paddingLeft: '18px' }}>
            <div style={{ textTransform: 'capitalize', textAlign: 'right' }}>
              <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#0F172A' }}>
                {user.profile?.name || user.profile?.hospital_name || user.email.split('@')[0]}
              </div>
              <span style={{
                fontSize: '0.7rem',
                fontWeight: 700,
                backgroundColor: '#DBEAFE',
                color: '#1E40AF',
                padding: '2px 8px',
                borderRadius: '4px'
              }}>
                {user.role?.toUpperCase()}
              </span>
            </div>
            <button
              onClick={() => { logout(); navigate('/'); }}
              style={{
                backgroundColor: '#FEF2F2',
                color: '#DC2626',
                border: '1px solid #FCA5A5',
                padding: '7px 14px',
                borderRadius: '6px',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
              }}
            >
              <LogOut size={16} /> Logout
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '10px' }}>
            <Link to="/login" style={{
              textDecoration: 'none',
              backgroundColor: '#DC2626',
              color: '#FFFFFF',
              padding: '8px 16px',
              borderRadius: '6px',
              fontWeight: 600
            }}>
              Sign In
            </Link>
            <Link to="/register" style={{
              textDecoration: 'none',
              backgroundColor: '#F1F5F9',
              color: '#334155',
              padding: '8px 16px',
              borderRadius: '6px',
              fontWeight: 600,
              border: '1px solid #CBD5E1'
            }}>
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};
