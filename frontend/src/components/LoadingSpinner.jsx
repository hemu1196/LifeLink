import React from 'react';

export const LoadingSpinner = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '40px' }}>
    <div style={{
      width: '40px',
      height: '40px',
      border: '4px solid #FEF2F2',
      borderTop: '4px solid #DC2626',
      borderRadius: '50%',
      animation: 'spin 1s linear infinite'
    }}></div>
    <style>{`
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);
