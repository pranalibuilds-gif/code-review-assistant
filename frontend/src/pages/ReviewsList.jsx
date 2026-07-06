import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, Filter, Trash2, ChevronRight, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';
import { getReviews } from '../api/reviews';
import Card from '../components/Card';
import Button from '../components/Button';
import SeverityBadge from '../components/SeverityBadge';

const ReviewsList = () => {
  const [search, setSearch] = useState('');

  const { data: reviews, isLoading } = useQuery({
    queryKey: ['reviews', search],
    queryFn: async () => {
      // For now, the backend might not support search/filter yet,
      // so we'll just list all and filter on frontend for demo.
      const res = await getReviews();
      return res.data;
    }
  });

  const filteredReviews = reviews?.filter(r =>
    r.project_name?.toLowerCase().includes(search.toLowerCase()) ||
    r.grade?.toLowerCase().includes(search.toLowerCase())
  ) || [];

  if (isLoading) return <div className="p-8">Loading History...</div>;

  return (
    <div className="space-y-8 pb-12">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <h1 className="text-3xl font-bold">Review History</h1>
        <div className="flex items-center gap-3">
           <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
              <input
                type="text"
                className="pl-10 pr-4 py-2 bg-slate-900 border border-slate-800 rounded-2xl outline-none w-64"
                placeholder="Search projects..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
           </div>
           <Button variant="secondary">
              <Filter size={18} className="mr-2" /> Filter
           </Button>
        </div>
      </div>

      <Card className="overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-slate-900 border-b border-slate-800">
            <tr>
              <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted">Project</th>
              <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted">Date</th>
              <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted">Score</th>
              <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted">Issues</th>
              <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-text-muted text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-border">
            {filteredReviews.length > 0 ? filteredReviews.map((review) => (
              <tr key={review.review_id} className="hover:bg-slate-900 transition-colors group">
                <td className="px-6 py-4">
                   <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded bg-primary-soft flex items-center justify-center text-primary-main">
                        <FileText size={16} />
                      </div>
                      <span className="font-bold text-text-base">{review.project_name || 'Quick Review'}</span>
                   </div>
                </td>
                <td className="px-6 py-4 text-sm text-text-muted">
                  {new Date(review.created_at).toLocaleDateString()}
                </td>
                <td className="px-6 py-4">
                   <div className="flex items-center gap-2">
                      <span className="font-bold text-lg">{Math.round(review.score)}</span>
                      <span className="text-[10px] font-black bg-slate-800 px-1.5 py-0.5 rounded border border-slate-700 uppercase">
                        {review.grade}
                      </span>
                   </div>
                </td>
                <td className="px-6 py-4">
                   <div className="flex gap-1">
                      {review.statistics?.critical_count > 0 && <div className="w-2 h-2 rounded-full bg-red-500" />}
                      {review.statistics?.high_count > 0 && <div className="w-2 h-2 rounded-full bg-orange-500" />}
                      <span className="text-xs text-text-muted ml-1">{review.statistics?.total_findings} items</span>
                   </div>
                </td>
                <td className="px-6 py-4 text-right">
                   <div className="flex justify-end gap-2">
                      <Link to={`/app/reviews/${review.review_id}`}>
                         <Button variant="ghost" size="sm">
                            View <ChevronRight size={14} className="ml-1" />
                         </Button>
                      </Link>
                      <button className="p-2 text-slate-300 hover:text-status-error transition-colors">
                        <Trash2 size={16} />
                      </button>
                   </div>
                </td>
              </tr>
            )) : (
              <tr>
                <td colSpan="5" className="px-6 py-20 text-center text-text-muted italic">
                   No reviews found matching your criteria.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </Card>
    </div>
  );
};

export default ReviewsList;
