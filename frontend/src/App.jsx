import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';

// Pages
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

// Donor Pages
import { DonorDashboard } from './pages/Donor/DonorDashboard';
import { DonorProfile } from './pages/Donor/DonorProfile';
import { EligibilityCheck } from './pages/Donor/EligibilityCheck';
import { MyResponses } from './pages/Donor/MyResponses';
import { DonationHistory } from './pages/Donor/DonationHistory';

// Hospital Pages
import { HospitalDashboard } from './pages/Hospital/HospitalDashboard';
import { CreateRequest } from './pages/Hospital/CreateRequest';
import { ManageRequests } from './pages/Hospital/ManageRequests';
import { DonorResponses } from './pages/Hospital/DonorResponses';

// Blood Bank Pages
import { BloodBankDashboard } from './pages/BloodBank/BloodBankDashboard';
import { AddStock } from './pages/BloodBank/AddStock';
import { InventoryManager } from './pages/BloodBank/InventoryManager';

// Admin Pages
import { AdminDashboard } from './pages/Admin/AdminDashboard';
import { HospitalVerification } from './pages/Admin/HospitalVerification';

// Standalone Pages
import { SmartMatchPage } from './pages/SmartMatchPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { NotificationsPage } from './pages/NotificationsPage';

const AppLayout = ({ children }) => (
  <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
    <Navbar />
    <div style={{ display: 'flex', flex: 1 }}>
      <Sidebar />
      <main style={{ flex: 1, padding: '24px', backgroundColor: '#F8FAFC' }}>
        {children}
      </main>
    </div>
  </div>
);

export const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppLayout>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/smart-match" element={<SmartMatchPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/notifications" element={<NotificationsPage />} />

            {/* Donor Routes */}
            <Route path="/donor/dashboard" element={<DonorDashboard />} />
            <Route path="/donor/profile" element={<DonorProfile />} />
            <Route path="/donor/eligibility" element={<EligibilityCheck />} />
            <Route path="/donor/responses" element={<MyResponses />} />
            <Route path="/donor/history" element={<DonationHistory />} />

            {/* Hospital Routes */}
            <Route path="/hospital/dashboard" element={<HospitalDashboard />} />
            <Route path="/hospital/create-request" element={<CreateRequest />} />
            <Route path="/hospital/manage-requests" element={<ManageRequests />} />
            <Route path="/hospital/responses" element={<DonorResponses />} />

            {/* Blood Bank Routes */}
            <Route path="/blood-bank/dashboard" element={<BloodBankDashboard />} />
            <Route path="/blood-bank/add-stock" element={<AddStock />} />
            <Route path="/blood-bank/inventory" element={<InventoryManager />} />

            {/* Admin Routes */}
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
            <Route path="/admin/verifications" element={<HospitalVerification />} />
          </Routes>
        </AppLayout>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
