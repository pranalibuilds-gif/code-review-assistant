import React from 'react';
import { Sparkles, ArrowRight } from 'lucide-react';
import Card from './Card';
import Button from './Button';

const AIInsightCard = ({ insight }) => {
  if (!insight) return null;

  return (
    <Card className="p-6 bg-gradient-to-br from-primary-main to-indigo-700 text-white border-none">
      <div className="flex items-center gap-2 mb-4 text-primary-soft">
        <Sparkles size={18} />
        <span className="text-xs font-bold uppercase tracking-widest">Mentor Recommendation</span>
      </div>

      <h3 className="text-xl font-bold mb-2">
        {insight.title || "Refactoring Opportunity"}
      </h3>

      <p className="text-primary-soft text-sm leading-relaxed mb-6">
        {insight.description || "The AI is currently analyzing your recent patterns to provide actionable advice."}
      </p>

      <Button
        variant="secondary"
        size="sm"
        className="bg-white/10 border-white/20 text-white hover:bg-white/20"
      >
        View Detail <ArrowRight size={14} className="ml-2" />
      </Button>
    </Card>
  );
};

export default AIInsightCard;
