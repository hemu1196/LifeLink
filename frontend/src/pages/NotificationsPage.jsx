import React, { useState, useEffect } from 'react';
import { notificationsAPI } from '../services/api';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { Bell, Check } from 'lucide-react';

export const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchNotifs = async () => {
    try {
      const res = await notificationsAPI.getNotifications();
      setNotifications(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifs();
  }, []);

  const handleMarkRead = async (id) => {
    try {
      await notificationsAPI.markAsRead(id);
      fetchNotifs();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '24px' }}>
      <div style={{
        background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
        color: 'white',
        padding: '30px',
        borderRadius: '16px',
        marginBottom: '25px'
      }}>
        <h1 style={{ margin: 0, fontSize: '2.2rem', fontWeight: 800 }}>🔔 IN-APP NOTIFICATIONS</h1>
        <p style={{ margin: '6px 0 0 0', color: '#D1FAE5' }}>
          Real-time alerts for emergency blood requests, donor responses & donation updates.
        </p>
      </div>

      {notifications.length === 0 ? (
        <div style={{ backgroundColor: '#FFFFFF', padding: '30px', textAlign: 'center', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
          <p style={{ color: '#64748B', margin: 0 }}>🎉 You have no notifications right now.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {notifications.map((n) => (
            <div key={n.id} style={{
              backgroundColor: n.read_status === 0 ? '#FEF2F2' : '#FFFFFF',
              border: n.read_status === 0 ? '1px solid #FCA5A5' : '1px solid #E2E8F0',
              padding: '16px',
              borderRadius: '10px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}>
              <div>
                <h4 style={{ margin: '0 0 4px 0', color: '#0F172A' }}>{n.title}</h4>
                <p style={{ margin: 0, color: '#334155', fontSize: '0.9rem' }}>{n.message}</p>
                <small style={{ color: '#64748B', marginTop: '4px', display: 'block' }}>{new Date(n.created_at).toLocaleString()}</small>
              </div>

              {n.read_status === 0 && (
                <button
                  onClick={() => handleMarkRead(n.id)}
                  style={{ backgroundColor: '#16A34A', color: 'white', border: 'none', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem', fontWeight: 600 }}
                >
                  <Check size={14} /> Mark Read
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
