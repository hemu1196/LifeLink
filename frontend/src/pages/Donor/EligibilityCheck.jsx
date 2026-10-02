import React, { useState, useEffect } from 'react';
import { donorAPI } from '../../services/api';
import { CheckCircle2, XCircle } from 'lucide-react';

export const EligibilityCheck = () => {
  const [eligibility, setEligibility] = useState(null);
  const [weight, setWeight] = useState(65);
  const [noIllness, setNoIllness] = useState(true);
  const [noTattoo, setNoTattoo] = useState(true);
  const [noMeds, setNoMeds] = useState(true);

  useEffect(() => {
    donorAPI.getEligibility().then((res) => setEligibility(res.data));
  }, []);

  const isWeightValid = weight >= 50;
  const isFullyEligible = eligibility?.eligible && isWeightValid && noIllness && noTattoo && noMeds;

  return (
    <div style={{ maxWidth: '700px' }}>
      <h2 style={{ marginBottom: '8px' }}>🩺 Smart Donor Eligibility Calculator</h2>
      <p style={{ color: '#64748B', marginBottom: '24px' }}>Verify your medical donation eligibility according to clinical criteria.</p>

      <div style={{ backgroundColor: '#FFFFFF', padding: '24px', borderRadius: '12px', border: '1px solid #E2E8F0', marginBottom: '24px' }}>
        <h3 style={{ margin: '0 0 16px 0' }}>Health Questionnaire</h3>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: 600, fontSize: '0.9rem', marginBottom: '4px' }}>Body Weight (kg)</label>
          <input type="number" value={weight} onChange={(e) => setWeight(Number(e.target.value))} style={{ width: '100%', padding: '8px 12px', borderRadius: '6px', border: '1px solid #CBD5E1', boxSizing: 'border-box' }} />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '16px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <input type="checkbox" checked={noIllness} onChange={(e) => setNoIllness(e.target.checked)} />
            <span>I have NOT had a fever, cold, or flu in the past 14 days.</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <input type="checkbox" checked={noTattoo} onChange={(e) => setNoTattoo(e.target.checked)} />
            <span>I have NOT received tattoos or major surgery in the past 6 months.</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <input type="checkbox" checked={noMeds} onChange={(e) => setNoMeds(e.target.checked)} />
            <span>I am NOT taking major antibiotics or blood thinners.</span>
          </label>
        </div>
      </div>

      {isFullyEligible ? (
        <div style={{ backgroundColor: '#F0FDF4', border: '1px solid #86EFAC', padding: '20px', borderRadius: '12px', color: '#166534' }}>
          <h3 style={{ margin: '0 0 8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckCircle2 size={24} color="#166534" /> You are FULLY ELIGIBLE to Donate Blood Today!
          </h3>
          <p style={{ margin: 0 }}>Your last donation status: {eligibility?.message}</p>
        </div>
      ) : (
        <div style={{ backgroundColor: '#FEF2F2', border: '1px solid #FCA5A5', padding: '20px', borderRadius: '12px', color: '#991B1B' }}>
          <h3 style={{ margin: '0 0 8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <XCircle size={24} color="#991B1B" /> Temporarily Ineligible to Donate
          </h3>
          <ul style={{ margin: '8px 0 0 0', paddingLeft: '20px' }}>
            {!eligibility?.eligible && <li>{eligibility?.message}</li>}
            {!isWeightValid && <li>Weight must be at least 50 kg (Current: {weight} kg).</li>}
            {!noIllness && <li>Must be free from recent fever/flu for 14 days.</li>}
            {!noTattoo && <li>Must wait 6 months post-tattoo or major surgery.</li>}
            {!noMeds && <li>Must not be taking active antibiotics/thinners.</li>}
          </ul>
        </div>
      )}
    </div>
  );
};
