import React from 'react';
import { clsx } from 'clsx';

const SeverityBadge = ({ severity }) => {
  const styles = {
    CRITICAL: 'bg-red-500/10 text-red-400 border-red-500/10',
    HIGH: 'bg-orange-500/10 text-orange-300 border-orange-500/10',
    MEDIUM: 'bg-amber-500/10 text-amber-300 border-amber-500/10',
    LOW: 'bg-sky-500/10 text-sky-300 border-sky-500/10',
    INFO: 'bg-slate-700 text-slate-200 border-slate-700',
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
