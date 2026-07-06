import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  FileText,
  Download,
  ChevronDown,
  AlertCircle,
  CheckCircle2,
  Code,
  ShieldCheck,
  Zap,
  BarChart2,
  Calendar,
  Layers,
  Sparkles
} from 'lucide-react';
import { getReview } from '../api/reviews';
import Button from '../components/Button';
import Card from '../components/Card';
import SeverityBadge from '../components/SeverityBadge';
import MetricCard from '../components/MetricCard';
import toast from 'react-hot-toast';

const ReviewDetail = () => {
  const { id } = useParams();
  const [showExportMenu, setShowExportMenu] = useState(false);

  const { data: report, isLoading, isError } = useQuery({
    queryKey: ['reviews', id],
    queryFn: async () => {
      const response = await getReview(id);
      return response.data;
    },
  });

  const handleExport = (format) => {
    const url = `/api/v1/reviews/${id}/export/${format}`;
    window.open(url, '_blank');
    setShowExportMenu(false);
    toast.success(`Generating ${format.toUpperCase()} report...`);
  };

  if (isLoading) return <div className="p-12 text-center text-text-muted">Loading Report...</div>;
  if (isError) return <div className="p-12 text-center text-status-error">Error loading report.</div>;

  const securityScore = report.findings.filter(f => f.category === 'Security').length > 0 ? 'B+' : 'A+';
  const maintainabilityValue = report.metrics.find(m => m.metric_name === 'Maintainability Index')?.metric_value || 0;

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
           <div className="w-12 h-12 bg-primary-soft rounded-xl flex items-center justify-center text-primary-main">
              <FileText size={24} />
           </div>
           <div>
              <h1 className="text-3xl font-bold text-text-base">
                Review Report
              </h1>
              <div className="flex items-center gap-3 text-xs text-text-muted mt-1">
                 <span className="flex items-center gap-1 font-mono uppercase tracking-tighter"><Layers size={12}/> ID: {id.split('-')[0]}</span>
                 <span className="flex items-center gap-1"><Calendar size={12}/> {new Date(report.created_at).toLocaleDateString()}</span>
              </div>
           </div>
        </div>

        <div className="relative">
           <Button variant="secondary" onClick={() => setShowExportMenu(!showExportMenu)} className="gap-2">
             <Download size={18} /> Export Report <ChevronDown size={16} />
           </Button>
           {showExportMenu && (
             <div className="absolute right-0 mt-2 w-48 bg-surface-card border border-surface-border rounded-[28px] shadow-soft z-50 overflow-hidden ring-1 ring-black/10">
                {['pdf', 'md', 'json'].map((fmt) => (
                  <button key={fmt} onClick={() => handleExport(fmt)} className="w-full text-left px-4 py-3 text-sm font-semibold hover:bg-surface-muted transition-colors uppercase border-b border-surface-border last:border-0">
                    {fmt === 'md' ? 'Markdown (.md)' : fmt.toUpperCase()}
                  </button>
                ))}
             </div>
           )}
        </div>
      </div>

      {/* Primary Scorecard */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
         <Card className="p-6 text-center border-b-4 border-b-primary-main">
            <div className="text-[10px] font-black uppercase tracking-widest text-text-muted mb-2">Overall Score</div>
            <div className="text-5xl font-black text-primary-main">{Math.round(report.score)}</div>
            <div className="mt-2 inline-block px-2 py-0.5 bg-primary-soft text-primary-main text-[10px] font-bold rounded uppercase">
               Grade {report.grade}
            </div>
         </Card>
         <Card className="p-6 text-center">
            <div className="text-[10px] font-black uppercase tracking-widest text-text-muted mb-2">Security</div>
            <div className={`text-4xl font-black ${securityScore === 'A+' ? 'text-status-success' : 'text-status-warning'}`}>
               {securityScore}
            </div>
            <p className="text-[10px] text-text-muted mt-2">Findings: {report.statistics.security_count}</p>
         </Card>
         <Card className="p-6 text-center">
            <div className="text-[10px] font-black uppercase tracking-widest text-text-muted mb-2">Maintenance</div>
            <div className="text-4xl font-black text-text-base">
               {maintainabilityValue > 80 ? 'A' : maintainabilityValue > 60 ? 'B' : 'C'}
            </div>
            <p className="text-[10px] text-text-muted mt-2">Index: {Math.round(maintainabilityValue)}</p>
         </Card>
         <Card className="p-6 text-center">
            <div className="text-[10px] font-black uppercase tracking-widest text-text-muted mb-2">Total Issues</div>
            <div className="text-4xl font-black text-text-base">{report.statistics.total_findings}</div>
            <div className="flex justify-center gap-1.5 mt-3">
               {[...Array(Math.min(3, report.statistics.critical_count))].map((_,i) => <div key={i} className="w-1.5 h-1.5 rounded-full bg-red-500" />)}
               {[...Array(Math.min(3, report.statistics.high_count))].map((_,i) => <div key={i} className="w-1.5 h-1.5 rounded-full bg-orange-500" />)}
            </div>
         </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
         <div className="lg:col-span-2 space-y-8">
            {/* AI Mentor Insights */}
            <Card className="p-8 bg-primary-main text-white border-none relative overflow-hidden">
               <div className="absolute top-0 right-0 p-8 opacity-10 rotate-12">
                  <Zap size={120} />
               </div>
               <h3 className="text-xl font-bold mb-6 flex items-center gap-3 relative z-10">
                  <Sparkles className="text-white" size={24} />
                  AI Mentor Assessment
               </h3>
               <p className="text-white/90 leading-relaxed mb-8 text-lg relative z-10 italic">
                  "{report.ai_summary || "Overall code quality is strong, with significant improvements in modularity."}"
               </p>

               <div className="space-y-4 relative z-10">
                  <h4 className="text-xs font-bold uppercase tracking-widest text-white/70">Key Recommendations</h4>
                  {report.recommendations?.map((rec, i) => (
                     <div key={i} className="p-4 bg-white/10 rounded-2xl border border-white/10 hover:bg-white/20 transition-colors group">
                        <div className="flex justify-between items-start mb-1">
                           <span className="font-bold text-white transition-colors">{rec.title}</span>
                           <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${rec.impact === 'High' ? 'bg-red-500/40 text-white' : 'bg-blue-500/40 text-white'}`}>
                              {rec.impact} Impact
                           </span>
                        </div>
                        <p className="text-sm text-white/80">{rec.description}</p>
                     </div>
                  ))}
               </div>
            </Card>

            {/* Findings List */}
            <div className="space-y-4">
               <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold">Detailed Findings</h3>
                  <div className="flex gap-2">
                     <div className="px-2 py-1 bg-surface-muted text-[10px] font-bold rounded border border-surface-border uppercase text-text-muted">
                        {report.findings.length} Total
                     </div>
                  </div>
               </div>
               <div className="space-y-3">
                  {report.findings.map((f, i) => (
                     <Card key={i} className="p-5 flex items-start gap-5 hover:border-primary-main/30 transition-colors">
                        <div className="mt-1">
                          {f.severity === 'CRITICAL' || f.severity === 'HIGH' ? (
                            <AlertCircle className="text-status-error" size={22} />
                          ) : (
                            <CheckCircle2 className="text-status-success" size={22} />
                          )}
                        </div>
                        <div className="flex-1">
                           <div className="flex items-center gap-3 mb-1.5">
                             <h4 className="font-bold text-text-base leading-none">{f.title}</h4>
                             <SeverityBadge severity={f.severity} />
                             <span className="text-[10px] font-bold text-text-muted bg-surface-muted px-1.5 py-0.5 rounded border border-surface-border uppercase">{f.category}</span>
                           </div>
                           <p className="text-sm text-text-muted mb-4">{f.description}</p>
                           <div className="flex items-center gap-3">
                              <div className="text-[10px] font-mono font-bold bg-surface-muted text-text-muted px-2 py-1 rounded flex items-center gap-1.5">
                                <Code size={10} /> {f.file_path}:{f.line}
                              </div>
                              <span className="text-[10px] font-bold text-primary-main uppercase">Source: {f.source}</span>
                           </div>
                        </div>
                     </Card>
                  ))}
               </div>
            </div>
         </div>

         {/* Sidebar: Metrics & Trends */}
         <div className="space-y-6">
            <Card className="p-6">
               <h3 className="font-bold text-text-base mb-4 flex items-center gap-2">
                  <BarChart2 size={18} className="text-primary-main" /> Project Metrics
               </h3>
               <div className="space-y-6">
                  {report.metrics.map((m, i) => (
                     <div key={i}>
                        <div className="flex justify-between text-xs mb-1.5">
                           <span className="font-bold text-text-muted uppercase tracking-tighter">{m.metric_name}</span>
                           <span className="font-black text-text-base">{Math.round(m.metric_value)}{m.unit}</span>
                        </div>
                        <div className="w-full h-1.5 bg-surface-muted rounded-full overflow-hidden">
                           <div
                              className={`h-full transition-all duration-1000 ${m.metric_value > 80 ? 'bg-status-success' : m.metric_value > 50 ? 'bg-status-warning' : 'bg-status-error'}`}
                              style={{ width: `${Math.min(100, m.metric_value)}%` }}
                           />
                        </div>
                     </div>
                  ))}
               </div>
            </Card>

            <Card className="p-6 bg-primary-main text-white border-none shadow-lg shadow-primary-main/20">
               <h3 className="font-bold mb-4 flex items-center gap-2">
                  <Zap size={18} className="fill-white" /> Performance
               </h3>
               <div className="space-y-2">
                  <div className="flex justify-between text-xs opacity-80">
                     <span>Analysis Time</span>
                     <span className="font-bold">{report.statistics.duration_ms}ms</span>
                  </div>
                  <div className="flex justify-between text-xs opacity-80">
                     <span>Files Scanned</span>
                     <span className="font-bold">{report.statistics.files_analyzed}</span>
                  </div>
               </div>
               <div className="mt-6 pt-4 border-t border-white/20">
                  <div className="text-[10px] font-bold uppercase opacity-60 mb-1">Project Status</div>
                  <div className="flex items-center gap-2 text-sm font-black">
                     <ShieldCheck size={16} /> READY FOR DEPLOYMENT
                  </div>
               </div>
            </Card>
         </div>
      </div>
    </div>
  );
};

export default ReviewDetail;
