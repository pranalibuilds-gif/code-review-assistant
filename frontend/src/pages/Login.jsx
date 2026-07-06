import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Button from '../components/Button';
import Card from '../components/Card';
import { Shield, Mail, Lock } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await login(email, password);
      navigate('/app/dashboard');
    } catch (error) {
      // Error handled by interceptor (toast)
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-app flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center gap-2 mb-8">
           <div className="w-12 h-12 bg-primary-main rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary-main/20">
              <Shield size={28} />
           </div>
           <h1 className="text-3xl font-bold text-text-base">CodeSage</h1>
           <p className="text-text-muted">Analyze. Improve. Evolve.</p>
        </div>

        <Card className="p-8">
           <h2 className="text-xl font-bold mb-6">Welcome Back</h2>
           <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                 <label className="block text-sm font-semibold text-text-base mb-1.5">Email Address</label>
                 <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      type="email"
                      required
                      className="w-full pl-10 pr-4 py-2.5 bg-surface-app border border-surface-border rounded-2xl focus:ring-2 focus:ring-primary-main/20 focus:border-primary-main outline-none transition-all text-text-base"
                      placeholder="dev@example.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                 </div>
              </div>

              <div>
                 <label className="block text-sm font-semibold text-text-base mb-1.5">Password</label>
                 <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      type="password"
                      required
                      className="w-full pl-10 pr-4 py-2.5 bg-surface-app border border-surface-border rounded-2xl focus:ring-2 focus:ring-primary-main/20 focus:border-primary-main outline-none transition-all text-text-base"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                 </div>
              </div>

              <Button
                type="submit"
                className="w-full h-11"
                isLoading={isLoading}
              >
                Sign In
              </Button>
           </form>

           <div className="mt-8 pt-6 border-t border-surface-border text-center">
              <p className="text-sm text-text-muted">
                Don't have an account? <Link to="/register" className="text-primary-main font-bold hover:underline">Register</Link>
              </p>
           </div>
        </Card>

        <p className="mt-8 text-center text-xs text-text-muted font-medium uppercase tracking-widest">
           System Administrator: admin@codesage.local
        </p>
      </div>
    </div>
  );
};

export default Login;
