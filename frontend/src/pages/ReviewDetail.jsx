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
  Zap
} from 'lucide-react';
import { getReview } from '../api/reviews';
import Button from '../components/Button';
import Card from '../components/Card';
import SeverityBadge from '../components/SeverityBadge';
import toast from 'react-hot-toast';

const ReviewDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
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

  if (isLoading) return <div className="animate-pulse">Loading Report...</div>;
  if (isError) return <div>Error loading report.</div>;

  return (
    <div className="space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
           <div className="flex items-center gap-2 text-text-muted text-sm mb-1">
              <FileText size={14} /> Review Report
           </div>
           <h1 className="text-3xl font-bold text-text-base">
             {report.project_name || 'Analysis Results'}
           </h1>
        </div>

        <div className="flex items-center gap-3 relative">
           <div className="relative">
              <Button
                variant="secondary"
                onClick={() => setShowExportMenu(!showExportMenu)}
                className="gap-2"
              >
                <Download size={18} /> Export <ChevronDown size={16} />
              </Button>

              {showExportMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-surface-card border border-surface-border rounded-lg shadow-xl z-50 overflow-hidden">
                   {['pdf', 'md', 'json'].map((fmt) => (
                     <button
                       key={fmt}
                       onClick={() => handleExport(fmt)}
                       className="w-full text-left px-4 py-3 text-sm font-medium hover:bg-slate-50 transition-colors uppercase border-b border-surface-border last:border-0"
                     >
                       {fmt === 'md' ? 'Markdown (.md)' : fmt.toUpperCase()}
                     </button>
                   ))}
                </div>
              )}
           </div>
        </div>
      </div>

      {/* Hero Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
         <Card className="p-6 text-center">
            <div className="text-[10px] font-bold uppercase tracking-widest text-text-muted mb-1">Overall Score</div>
            <div className="text-4xl font-black text-primary-main">{Math.round(report.score)}</div>
            <div className="text-xs font-bold text-primary-main/60 mt-1">Grade {report.grade}</div>
         </Card>
         <Card className="p-6 text-center">
            <div className="text-[10px] font-bold uppercase tracking-widest text-text-muted mb-1">Total Issues</div>
            <div className="text-4xl font-black text-text-base">{report.statistics.total_findings}</div>
            <div className="flex justify-center gap-2 mt-2">
               <span className="w-2 h-2 rounded-full bg-red-500" />
               <span className="w-2 h-2 rounded-full bg-orange-500" />
               <span className="w-2 h-2 rounded-full bg-yellow-500" />
            </div>
         </Card>
         <Card className="p-6 text-center">
            <div className="text-[10px] font-bold uppercase tracking-widest text-text-muted mb-1">Security</div>
            <div className="text-4xl font-black text-status-success">A+</div>
         </Card>
         <Card className="p-6 text-center">
            <div className="text-[10px] font-bold uppercase tracking-widest text-text-muted mb-1">Maintenance</div>
            <div className="text-4xl font-black text-status-warning">B</div>
         </Card>
      </div>

      {/* AI Mentor Summary */}
      <Card className="p-8 border-l-4 border-l-primary-main">
         <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
            <Zap size={20} className="text-primary-main fill-primary-main" /> AI Mentor Summary
         </h3>
         <p className="text-text-base leading-relaxed">
            {report.ai_summary || report.summary}
         </p>
      </Card>

      {/* Findings List (Simplified for Export Phase) */}
      <div className="space-y-4">
         <h3 className="text-xl font-bold">Detailed Findings</h3>
         {report.findings.map((f, i) => (
            <Card key={i} className="p-4 flex items-start gap-4">
               <div className="mt-1">
                 {f.severity === 'CRITICAL' || f.severity === 'HIGH' ? (
                   <AlertCircle className="text-status-error" size={20} />
                 ) : (
                   <CheckCircle2 className="text-status-success" size={20} />
                 )}
               </div>
               <div className="flex-1">
                  <div className="flex items-center gap-3 mb-1">
                    <h4 className="font-bold text-text-base">{f.title}</h4>
                    <SeverityBadge severity={f.severity} />
                  </div>
                  <p className="text-sm text-text-muted mb-2">{f.description}</p>
                  <div className="text-[10px] font-mono bg-slate-50 px-2 py-1 rounded inline-block border border-slate-200">
                    {f.file_path}:{f.line}
                  </div>
               </div>
            </Card>
         ))}
      </div>
    </div>
  );
};

export default ReviewDetail;
