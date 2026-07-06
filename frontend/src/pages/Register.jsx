import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register as apiRegister } from '../api/auth';
import Button from '../components/Button';
import Card from '../components/Card';
import { Shield, Mail, Lock, User } from 'lucide-react';
import toast from 'react-hot-toast';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    full_name: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await apiRegister(formData);
      toast.success('Registration successful! Please sign in.');
      navigate('/login');
    } catch (error) {
      // Error handled by toast in interceptor
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-app flex items-center justify-center p-6 text-text-base">
      <div className="w-full max-w-md">
        <div className="flex flex-col items-center gap-2 mb-8">
           <div className="w-12 h-12 bg-primary-main rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary-main/20">
              <Shield size={28} />
           </div>
           <h1 className="text-3xl font-bold">CodeSage</h1>
           <p className="text-text-muted">Analyze. Improve. Evolve.</p>
        </div>

        <Card className="p-8">
           <h2 className="text-xl font-bold mb-6">Create Account</h2>
           <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                 <label className="block text-sm font-semibold mb-1.5">Full Name</label>
                 <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      name="full_name"
                      required
                      className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-surface-border rounded-lg outline-none focus:ring-2 focus:ring-primary-main/20 focus:border-primary-main transition-all"
                      placeholder="Jane Doe"
                      value={formData.full_name}
                      onChange={handleChange}
                    />
                 </div>
              </div>

              <div>
                 <label className="block text-sm font-semibold mb-1.5">Username</label>
                 <div className="relative">
                    <User className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      name="username"
                      required
                      className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-surface-border rounded-lg outline-none focus:ring-2 focus:ring-primary-main/20 focus:border-primary-main transition-all"
                      placeholder="janedev"
                      value={formData.username}
                      onChange={handleChange}
                    />
                 </div>
              </div>

              <div>
                 <label className="block text-sm font-semibold mb-1.5">Email Address</label>
                 <div className="relative">
                    <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      name="email"
                      type="email"
                      required
                      className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-surface-border rounded-lg outline-none focus:ring-2 focus:ring-primary-main/20 focus:border-primary-main transition-all"
                      placeholder="jane@example.com"
                      value={formData.email}
                      onChange={handleChange}
                    />
                 </div>
              </div>

              <div>
                 <label className="block text-sm font-semibold mb-1.5">Password (Min 8 chars)</label>
                 <div className="relative">
                    <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                    <input
                      name="password"
                      type="password"
                      required
                      minLength={8}
                      className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-surface-border rounded-lg outline-none focus:ring-2 focus:ring-primary-main/20 focus:border-primary-main transition-all"
                      placeholder="••••••••"
                      value={formData.password}
                      onChange={handleChange}
                    />
                 </div>
              </div>

              <Button
                type="submit"
                className="w-full h-11 mt-2"
                isLoading={isLoading}
              >
                Create Account
              </Button>
           </form>

           <div className="mt-8 pt-6 border-t border-surface-border text-center">
              <p className="text-sm text-text-muted">
                Already have an account? <Link to="/login" className="text-primary-main font-bold hover:underline">Sign In</Link>
              </p>
           </div>
        </Card>
      </div>
    </div>
  );
};

export default Register;
