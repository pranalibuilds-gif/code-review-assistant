import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  PlusCircle,
  History,
  Settings,
  ShieldCheck,
  LogOut,
  Menu,
  X,
  User
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useSystemHealth } from '../hooks/useSystem';
import { clsx } from 'clsx';
import StatusDot from '../components/StatusDot';

const SidebarItem = ({ icon: Icon, label, to, active, collapsed }) => (
  <Link
    to={to}
    className={clsx(
      'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors mb-1',
      active
        ? 'bg-primary-main text-white'
        : 'text-text-muted hover:bg-slate-100 hover:text-text-base'
    )}
  >
    <Icon size={20} className="shrink-0" />
    {!collapsed && <span className="font-medium text-sm whitespace-nowrap">{label}</span>}
  </Link>
);

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const { data: health } = useSystemHealth();
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', to: '/app/dashboard' },
    { icon: PlusCircle, label: 'New Review', to: '/app/new-review' },
    { icon: History, label: 'Reviews', to: '/app/reviews' },
    { icon: Settings, label: 'Settings', to: '/app/settings' },
  ];

  if (user?.role === 'admin') {
    navItems.push({ icon: ShieldCheck, label: 'Admin', to: '/app/admin' });
  }

  return (
    <div className="flex h-screen bg-surface-app overflow-hidden">
      {/* Sidebar */}
      <aside
        className={clsx(
          "bg-surface-card border-r border-surface-border flex flex-col transition-all duration-300",
          collapsed ? "w-20" : "w-64"
        )}
      >
        <div className="p-4 border-b border-surface-border flex items-center justify-between">
          {!collapsed && <span className="text-xl font-bold text-primary-main">CodeSage</span>}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1.5 hover:bg-slate-100 rounded-md text-text-muted"
          >
            {collapsed ? <Menu size={20} /> : <X size={20} />}
          </button>
        </div>

        <nav className="flex-1 p-3 overflow-y-auto">
          {navItems.map((item) => (
            <SidebarItem
              key={item.to}
              {...item}
              active={location.pathname === item.to}
              collapsed={collapsed}
            />
          ))}
        </nav>

        <div className="p-4 border-t border-surface-border">
          <div className={clsx("flex items-center gap-3", collapsed ? "justify-center" : "")}>
             <div className="w-8 h-8 rounded-full bg-primary-soft flex items-center justify-center text-primary-main">
                <User size={18} />
             </div>
             {!collapsed && (
               <div className="flex-1 min-w-0">
                 <p className="text-sm font-semibold text-text-base truncate">{user?.username}</p>
                 <p className="text-xs text-text-muted truncate">{user?.email}</p>
               </div>
             )}
          </div>
          <button
            onClick={handleLogout}
            className={clsx(
              "mt-4 flex items-center gap-3 w-full px-3 py-2 text-status-error hover:bg-red-50 rounded-lg transition-colors",
              collapsed ? "justify-center" : ""
            )}
          >
            <LogOut size={20} />
            {!collapsed && <span className="text-sm font-medium">Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden text-text-base">
        <header className="h-16 bg-surface-card border-b border-surface-border flex items-center px-8 shrink-0">
           <div className="flex-1">
              <h2 className="text-sm font-medium text-text-muted">
                {location.pathname.split('/').pop()?.replace('-', ' ')}
              </h2>
           </div>
           <div className="flex items-center gap-4">
              <div className={clsx(
                "flex items-center gap-2 px-3 py-1 text-xs font-medium rounded-full border",
                health?.status === 'online'
                  ? "bg-status-success/10 text-status-success border-status-success/20"
                  : "bg-status-error/10 text-status-error border-status-error/20"
              )}>
                <StatusDot status={health?.status === 'online' ? 'online' : 'offline'} />
                AI Service {health?.status === 'online' ? 'Online' : 'Offline'}
              </div>
           </div>
        </header>

        <div className="flex-1 overflow-y-auto p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
