import React from 'react';
import Card from './Card';

const MetricCard = ({ title, value, unit, icon: Icon, trend }) => {
  return (
    <Card className="p-5 flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-text-muted">{title}</span>
        {Icon && <Icon size={18} className="text-primary-main opacity-80" />}
      </div>
      <div className="flex items-baseline gap-1">
        <span className="text-2xl font-bold text-text-base">{value}</span>
        {unit && <span className="text-xs text-text-muted font-medium">{unit}</span>}
      </div>
      {trend !== undefined && (
        <div className={`text-xs font-semibold ${trend >= 0 ? 'text-status-success' : 'text-status-error'}`}>
          {trend >= 0 ? '▲' : '▼'} {Math.abs(trend)}%
        </div>
      )}
    </Card>
  );
};

export default MetricCard;
