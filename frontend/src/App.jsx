import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

import { AuthProvider, useAuth } from './contexts/AuthContext';
import DashboardLayout from './layouts/DashboardLayout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import ReviewDetail from './pages/ReviewDetail';
import Admin from './pages/Admin';

// Placeholder Pages
const NewReview = () => <div className="p-8">New Review Workflow Placeholder</div>;
const ReviewsList = () => <div className="p-8">Reviews History Placeholder</div>;
const Settings = () => <div className="p-8">Settings Placeholder</div>;

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-surface-app">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-main"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Public Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* App Routes */}
            <Route
              path="/app"
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="new-review" element={<NewReview />} />
              <Route path="reviews" element={<ReviewsList />} />
              <Route path="reviews/:id" element={<ReviewDetail />} />
              <Route path="settings" element={<Settings />} />
              <Route path="admin" element={<Admin />} />
              <Route index element={<Navigate to="dashboard" replace />} />
            </Route>

            {/* Redirects */}
            <Route path="/" element={<Navigate to="/app/dashboard" replace />} />
          </Routes>
          <Toaster position="top-right" />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
