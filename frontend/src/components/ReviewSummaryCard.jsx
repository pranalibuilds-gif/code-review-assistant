import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight, Calendar, AlertCircle } from 'lucide-react';
import Card from './Card';
import SeverityBadge from './SeverityBadge';

const ReviewSummaryCard = ({ review }) => {
  const date = new Date(review.created_at).toLocaleDateString();

  return (
    <Link to={`/app/reviews/${review.review_id}`}>
      <Card className="p-4 hover:border-primary-main/50 transition-all group">
        <div className="flex items-center justify-between">
          <div className="flex flex-col gap-1">
            <h4 className="font-bold text-text-base group-hover:text-primary-main transition-colors">
              {review.project_name || 'Project Analysis'}
            </h4>
            <div className="flex items-center gap-3 text-xs text-text-muted">
              <span className="flex items-center gap-1">
                <Calendar size={12} /> {date}
              </span>
              <span className="flex items-center gap-1">
                <AlertCircle size={12} /> {review.statistics?.total_findings || 0} issues
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
             <div className="text-right">
                <div className="text-lg font-bold text-primary-main">
                  {Math.round(review.score)}
                </div>
                <div className="text-[10px] font-bold uppercase tracking-wider text-text-muted">
                  Grade {review.grade}
                </div>
             </div>
             <ChevronRight size={18} className="text-text-muted group-hover:text-primary-main transition-colors" />
          </div>
        </div>
      </Card>
    </Link>
  );
};

export default ReviewSummaryCard;
