import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts';
import { Plus, LayoutDashboard, BarChart3, Activity } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

import { useDashboardSummary } from '../hooks/useDashboard';
import Button from '../components/Button';
import Card from '../components/Card';
import MetricCard from '../components/MetricCard';
import ReviewSummaryCard from '../components/ReviewSummaryCard';
import AIInsightCard from '../components/AIInsightCard';

const Dashboard = () => {
  const navigate = useNavigate();
  const { data, isLoading, isError } = useDashboardSummary();

  if (isLoading) {
    return <div className="animate-pulse space-y-8">
      <div className="h-40 bg-surface-muted rounded-xl" />
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="h-32 bg-surface-muted rounded-xl" />
        <div className="h-32 bg-surface-muted rounded-xl" />
        <div className="h-32 bg-surface-muted rounded-xl" />
      </div>
    </div>;
  }

  if (isError) {
    return (
      <Card className="p-12 text-center">
        <h3 className="text-xl font-bold text-status-error mb-2">Failed to load dashboard</h3>
        <p className="text-text-muted">Please check your connection and try again.</p>
        <Button className="mt-6" onClick={() => window.location.reload()}>Retry</Button>
      </Card>
    );
  }

  // Sample data for charts (In real app, this would come from the backend DTO)
  const qualityHistory = data?.recent_reviews?.map(r => ({
    name: new Date(r.created_at).toLocaleDateString(),
    score: Math.round(r.score)
  })).reverse() || [];

  const severityData = data?.severity_distribution ? [
    { name: 'Critical', value: data.severity_distribution.CRITICAL, color: '#991b1b' },
    { name: 'High', value: data.severity_distribution.HIGH, color: '#ea580c' },
    { name: 'Medium', value: data.severity_distribution.MEDIUM, color: '#eab308' },
    { name: 'Low', value: data.severity_distribution.LOW, color: '#2563eb' },
  ].filter(d => d.value > 0) : [];

  return (
    <div className="space-y-8 pb-12">
      {/* Top Row: Main Insight & Primary Action */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-2 p-6 flex flex-col gap-4">
          <div className="flex items-center justify-between mb-2">
             <h3 className="font-bold text-text-base flex items-center gap-2">
               <Activity size={18} className="text-primary-main" />
               Quality Trend
             </h3>
             <span className="text-xs font-semibold text-status-success bg-status-success/10 px-2 py-1 rounded">
               Improving
             </span>
          </div>
          <div className="h-[240px] w-full">
            {qualityHistory.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={qualityHistory}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--surface-border)" />
                  <XAxis
                    dataKey="name"
                    axisLine={false}
                    tickLine={false}
                    tick={{fontSize: 10, fill: 'var(--text-muted)'}}
                    dy={10}
                  />
                  <YAxis
                    domain={[0, 100]}
                    axisLine={false}
                    tickLine={false}
                    tick={{fontSize: 10, fill: 'var(--text-muted)'}}
                  />
                  <Tooltip
                    contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
                  />
                  <Line
                    type="monotone"
                    dataKey="score"
                    stroke="#6366f1"
                    strokeWidth={3}
                    dot={{ r: 4, fill: '#6366f1', strokeWidth: 2, stroke: '#fff' }}
                    activeDot={{ r: 6, strokeWidth: 0 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-text-muted text-sm italic">
                No history yet. Start your first review.
              </div>
            )}
          </div>
        </Card>

        <Card className="p-6 bg-primary-main text-white border-none flex flex-col justify-center gap-6">
           <div>
              <h2 className="text-2xl font-bold mb-2">Ready for a Review?</h2>
              <p className="text-white/80 text-sm">Submit your latest code and let CodeSage identify improvements.</p>
           </div>
           <Button
            size="lg"
            className="w-full h-14 text-lg"
            onClick={() => navigate('/app/new-review')}
           >
             <Plus size={20} className="mr-2" /> Start New Review
           </Button>
           <div className="grid grid-cols-2 gap-3">
              <button className="p-3 bg-white/5 rounded-lg text-xs font-medium hover:bg-white/10 transition-colors">
                Upload ZIP
              </button>
              <button className="p-3 bg-white/5 rounded-lg text-xs font-medium hover:bg-white/10 transition-colors">
                GitHub Repo
              </button>
           </div>
        </Card>
      </div>

      {/* Second Row: Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Average Score"
          value={data?.average_score || 0}
          unit="/ 100"
          icon={BarChart3}
        />
        <MetricCard
          title="Total Reviews"
          value={data?.total_reviews || 0}
          icon={LayoutDashboard}
        />
        <MetricCard
          title="Files Analyzed"
          value={142} // This should come from stats in real backend expansion
          unit="files"
          icon={Activity}
        />
        <MetricCard
          title="Issues Fixed"
          value={28}
          trend={+12}
        />
      </div>

      {/* Third Row: Recent Reviews & Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-4">
           <div className="flex items-center justify-between">
              <h3 className="font-bold text-text-base">Recent Reviews</h3>
              <Button variant="ghost" size="sm" onClick={() => navigate('/app/reviews')}>
                View All
              </Button>
           </div>
           <div className="space-y-3">
              {data?.recent_reviews?.length > 0 ? (
                data.recent_reviews.map((review) => (
                  <ReviewSummaryCard key={review.review_id} review={review} />
                ))
              ) : (
                <Card className="p-8 text-center border-dashed">
                  <p className="text-text-muted text-sm italic">No recent activity.</p>
                </Card>
              )}
           </div>
        </div>

        <div className="space-y-6">
           <Card className="p-6">
              <h3 className="font-bold text-text-base mb-4">Issue Distribution</h3>
              <div className="h-[200px] w-full">
                {severityData.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={severityData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {severityData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend verticalAlign="bottom" height={36}/>
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-full flex items-center justify-center text-text-muted text-sm italic text-center px-4">
                    No data to visualize yet.
                  </div>
                )}
              </div>
           </Card>

           <AIInsightCard
              insight={data?.recent_reviews?.[0]?.recommendations?.[0] || {
                title: "Refactor logic to services",
                description: "Several of your recent reviews show business logic inside route handlers. Move this to the Service layer to improve testability and reuse."
              }}
           />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
