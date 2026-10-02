import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, User, CheckCircle, Heart, History, PlusCircle, AlertCircle, Users, Droplet, Shield } from 'lucide-react';

export const Sidebar = () => {
  const { user } = useAuth();
  if (!user) return null;

  const role = user.role;

  const getNavItems = () => {
    switch (role) {
      case 'donor':
        return [
          { to: '/donor/dashboard', label: 'Dashboard', icon: LayoutDashboard },
          { to: '/donor/profile', label: 'My Profile', icon: User },
          { to: '/donor/eligibility', label: 'Eligibility Check', icon: CheckCircle },
          { to: '/donor/responses', label: 'My Responses', icon: Heart },
          { to: '/donor/history', label: 'Donation History', icon: History },
        ];
      case 'hospital':
        return [
          { to: '/hospital/dashboard', label: 'Dashboard', icon: LayoutDashboard },
          { to: '/hospital/create-request', label: 'Create Request', icon: PlusCircle },
          { to: '/hospital/manage-requests', label: 'Active Requests', icon: AlertCircle },
          { to: '/hospital/responses', label: 'Donor Responses', icon: Users },
        ];
      case 'blood_bank':
        return [
          { to: '/blood-bank/dashboard', label: 'Stock Overview', icon: LayoutDashboard },
          { to: '/blood-bank/add-stock', label: 'Add Blood Units', icon: PlusCircle },
          { to: '/blood-bank/inventory', label: 'Batch Inventory', icon: Droplet },
        ];
      case 'admin':
        return [
          { to: '/admin/dashboard', label: 'Admin Overview', icon: LayoutDashboard },
          { to: '/admin/verifications', label: 'Hospital Verifications', icon: Shield },
        ];
      default:
        return [];
    }
  };

  const navItems = getNavItems();

  return (
    <aside style={{
      width: '240px',
      backgroundColor: '#FFFFFF',
      borderRight: '1px solid #E2E8F0',
      minHeight: 'calc(100vh - 65px)',
      padding: '20px 14px',
      boxSizing: 'border-box'
    }}>
      <div style={{ fontSize: '0.75rem', fontWeight: 800, color: '#94A3B8', textTransform: 'uppercase', marginBottom: '14px', paddingLeft: '8px' }}>
        {role?.toUpperCase()} PORTAL
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              style={({ isActive }) => ({
                textDecoration: 'none',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                padding: '10px 12px',
                borderRadius: '8px',
                fontWeight: 600,
                fontSize: '0.9rem',
                color: isActive ? '#DC2626' : '#475569',
                backgroundColor: isActive ? '#FEF2F2' : 'transparent',
                borderLeft: isActive ? '3px solid #DC2626' : '3px solid transparent'
              })}
            >
              <Icon size={18} />
              {item.label}
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
};
