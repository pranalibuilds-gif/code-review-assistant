import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { User, Mail, Shield, Bell, Moon, Globe, Sun } from 'lucide-react';
import Card from '../components/Card';
import Button from '../components/Button';
import toast from 'react-hot-toast';

const Settings = () => {
  const { user } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    username: user?.username || ''
  });

  const handleSave = () => {
    toast.success('Profile updated successfully (Demo)');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12 text-text-base">
      <h1 className="text-3xl font-bold">Settings</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Left Column: Profile Card */}
        <Card className="p-6 text-center h-fit">
           <div className="w-24 h-24 bg-primary-soft rounded-full flex items-center justify-center text-primary-main mx-auto mb-4 border-4 border-surface-app shadow-sm">
              <User size={40} />
           </div>
           <h3 className="font-bold text-xl">{user?.full_name}</h3>
           <p className="text-text-muted text-sm capitalize">{user?.role}</p>

           <div className="mt-6 pt-6 border-t border-surface-border space-y-4">
              <div className="flex items-center gap-2 text-xs text-text-muted font-medium uppercase tracking-widest">
                 <Shield size={14} /> Security Status
              </div>
              <div className="px-3 py-1.5 bg-status-success/10 text-status-success text-xs font-bold rounded-lg border border-status-success/20">
                 Verified Account
              </div>
           </div>
        </Card>

        {/* Right Column: Detailed Settings */}
        <div className="md:col-span-2 space-y-6">
           <Card className="p-8">
              <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                 <User className="text-primary-main" size={20} /> Personal Information
              </h3>
              <div className="space-y-4">
                 <div className="grid grid-cols-2 gap-4">
                    <div>
                       <label className="block text-xs font-bold text-text-muted uppercase mb-1.5">Full Name</label>
                       <input
                        type="text"
                        className="w-full p-2.5 bg-surface-app border border-surface-border rounded-2xl outline-none focus:ring-2 focus:ring-primary-main/20 text-text-base"
                        value={formData.full_name}
                        onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                       />
                    </div>
                    <div>
                       <label className="block text-xs font-bold text-text-muted uppercase mb-1.5">Username</label>
                       <input
                        type="text"
                        className="w-full p-2.5 bg-surface-app border border-surface-border rounded-2xl outline-none focus:ring-2 focus:ring-primary-main/20 text-text-base"
                        value={formData.username}
                        readOnly
                       />
                    </div>
                 </div>
                 <div>
                    <label className="block text-xs font-bold text-text-muted uppercase mb-1.5">Email Address</label>
                    <input
                      type="email"
                      className="w-full p-2.5 bg-surface-app border border-surface-border rounded-2xl outline-none focus:ring-2 focus:ring-primary-main/20 text-text-base"
                      value={formData.email}
                      readOnly
                    />
                 </div>
                 <Button onClick={handleSave} className="mt-4">Update Profile</Button>
              </div>
           </Card>

           <Card className="p-8">
              <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                 <Globe className="text-primary-main" size={20} /> Preferences
              </h3>
              <div className="space-y-4">
                 <div className="flex items-center justify-between p-3 bg-surface-app rounded-2xl">
                    <div className="flex items-center gap-3">
                       {theme === 'dark' ? <Moon size={18} className="text-text-muted" /> : <Sun size={18} className="text-text-muted" />}
                       <span className="text-sm font-medium">Dark Mode</span>
                    </div>
                    <button
                      onClick={toggleTheme}
                      className={`w-10 h-5 rounded-full relative transition-colors ${theme === 'dark' ? 'bg-primary-main' : 'bg-slate-300'}`}
                    >
                       <div className={`w-3 h-3 bg-white rounded-full absolute top-1 transition-all ${theme === 'dark' ? 'right-1' : 'left-1'}`} />
                    </button>
                 </div>
                 <div className="flex items-center justify-between p-3 bg-surface-app rounded-2xl">
                    <div className="flex items-center gap-3">
                       <Bell size={18} className="text-text-muted" />
                       <span className="text-sm font-medium">Email Notifications</span>
                    </div>
                    <div className="w-10 h-5 bg-primary-main rounded-full relative cursor-pointer">
                       <div className="w-3 h-3 bg-white rounded-full absolute top-1 right-1" />
                    </div>
                 </div>
              </div>
           </Card>
        </div>
      </div>
    </div>
  );
};

export default Settings;
