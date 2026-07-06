import React from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import {
  ShieldCheck,
  Activity,
  Database,
  Cpu,
  HardDrive,
  History,
  Trash2,
  AlertTriangle,
  CheckCircle2
} from 'lucide-react';
import { getSystemHealth, getJobs, getAuditLogs, runMaintenanceCleanup } from '../api/admin';
import Card from '../components/Card';
import Button from '../components/Button';
import toast from 'react-hot-toast';

const HealthCard = ({ title, status, details, icon: Icon }) => (
  <Card className="p-5">
    <div className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg ${status === 'healthy' ? 'bg-status-success/10 text-status-success' : 'bg-status-warning/10 text-status-warning'}`}>
          <Icon size={20} />
        </div>
        <h4 className="font-bold text-text-base">{title}</h4>
      </div>
      <div className={`text-xs font-bold uppercase tracking-wider ${status === 'healthy' ? 'text-status-success' : 'text-status-warning'}`}>
        {status}
      </div>
    </div>
    <div className="space-y-1">
      {Object.entries(details).map(([key, val]) => (
        <div key={key} className="flex justify-between text-xs">
          <span className="text-text-muted capitalize">{key.replace('_', ' ')}</span>
          <span className="font-medium">{String(val)}</span>
        </div>
      ))}
    </div>
  </Card>
);

const Admin = () => {
  const healthQuery = useQuery({ queryKey: ['admin', 'health'], queryFn: getSystemHealth, refetchInterval: 10000 });
  const jobsQuery = useQuery({ queryKey: ['admin', 'jobs'], queryFn: getJobs, refetchInterval: 5000 });
  const auditQuery = useQuery({ queryKey: ['admin', 'audit'], queryFn: () => getAuditLogs({ limit: 10 }) });

  const cleanupMutation = useMutation({
    mutationFn: runMaintenanceCleanup,
    onSuccess: (data) => toast.success(data.message),
  });

  if (healthQuery.isLoading || jobsQuery.isLoading) return <div className="p-8">Loading Admin Dashboard...</div>;

  const health = healthQuery.data;
  const jobs = jobsQuery.data;

  return (
    <div className="space-y-8 pb-12">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          <ShieldCheck className="text-primary-main" size={32} />
          System Administration
        </h1>
        <Button
          variant="danger"
          size="sm"
          onClick={() => cleanupMutation.mutate()}
          isLoading={cleanupMutation.isPending}
        >
          <Trash2 size={16} className="mr-2" /> Run Cleanup
        </Button>
      </div>

      {/* Health Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <HealthCard
          title="Database"
          status={health.services.database.status}
          icon={Database}
          details={{ latency: `${health.services.database.latency_ms}ms` }}
        />
        <HealthCard
          title="AI Engine"
          status={health.services.ai.status}
          icon={Cpu}
          details={{ model: health.services.ai.model, provider: health.services.ai.provider }}
        />
        <HealthCard
          title="Storage"
          status={health.services.storage.status}
          icon={HardDrive}
          details={{ free: `${health.services.storage.free_gb}GB`, used: `${health.services.storage.percent_used}%` }}
        />
        <HealthCard
          title="API"
          status="healthy"
          icon={Activity}
          details={{ version: health.services.api.version, env: health.services.api.environment }}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Active Jobs */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <Activity size={20} className="text-primary-main" /> Active Pipeline
          </h3>
          <Card className="overflow-hidden">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-900 border-b border-slate-800">
                <tr>
                  <th className="px-4 py-3 font-bold">Job ID</th>
                  <th className="px-4 py-3 font-bold">Type</th>
                  <th className="px-4 py-3 font-bold">Status</th>
                  <th className="px-4 py-3 font-bold">Started</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-border">
                {jobs.jobs.length > 0 ? jobs.jobs.map(job => (
                  <tr key={job.submission_id}>
                    <td className="px-4 py-3 font-mono text-xs truncate max-w-[120px]">{job.submission_id}</td>
                    <td className="px-4 py-3">{job.type}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 bg-primary-soft text-primary-main rounded-full text-[10px] font-bold uppercase">
                        {job.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-text-muted">{new Date(job.created_at).toLocaleTimeString()}</td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="4" className="px-4 py-8 text-center text-text-muted italic">No active jobs.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </Card>
        </div>

        {/* Audit Logs */}
        <div className="space-y-4">
          <h3 className="text-xl font-bold flex items-center gap-2">
            <History size={20} className="text-primary-main" /> Recent Audit
          </h3>
          <Card className="p-4 space-y-4">
             {auditQuery.data?.map(log => (
               <div key={log.id} className="text-xs border-b border-surface-border pb-3 last:border-0">
                  <div className="flex justify-between mb-1">
                    <span className="font-bold text-text-base">{log.action}</span>
                    <span className="text-text-muted">{new Date(log.created_at).toLocaleTimeString()}</span>
                  </div>
                  <p className="text-text-muted truncate">{log.details}</p>
               </div>
             ))}
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Admin;
