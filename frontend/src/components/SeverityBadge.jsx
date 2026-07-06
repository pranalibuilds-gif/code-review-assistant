import React from 'react';
import { clsx } from 'clsx';

const SeverityBadge = ({ severity }) => {
  const styles = {
    CRITICAL: 'bg-red-100 text-red-800 border-red-200',
    HIGH: 'bg-orange-100 text-orange-800 border-orange-200',
    MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    LOW: 'bg-blue-100 text-blue-800 border-blue-200',
    INFO: 'bg-slate-100 text-slate-800 border-slate-200',
  };

  return (
    <span className={clsx(
      'px-2 py-0.5 rounded-full text-xs font-semibold border',
      styles[severity] || styles.INFO
    )}>
      {severity}
    </span>
  );
};

export default SeverityBadge;
