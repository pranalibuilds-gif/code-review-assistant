import React from 'react';
import { clsx } from 'clsx';

const StatusDot = ({ status = 'online' }) => {
  const styles = {
    online: 'bg-status-success',
    degraded: 'bg-status-warning',
    offline: 'bg-status-error',
    pending: 'bg-slate-400 animate-pulse',
  };

  return (
    <div className={clsx(
      'w-2 h-2 rounded-full',
      styles[status] || styles.offline
    )} />
  );
};

export default StatusDot;
