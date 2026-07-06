import client from './client';

export const getSystemHealth = () => client.get('/admin/health');
export const getJobs = () => client.get('/admin/jobs');
export const getAuditLogs = (params) => client.get('/admin/audit', { params });
export const runMaintenanceCleanup = () => client.post('/admin/maintenance/cleanup');
