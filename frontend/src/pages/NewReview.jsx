import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import {
  Plus,
  Code2,
  Upload,
  Github,
  Loader2,
  CheckCircle2,
  AlertCircle,
  FileCode,
  ArrowRight
} from 'lucide-react';
import toast from 'react-hot-toast';

import { getProjects, createProject } from '../api/projects';
import { submitPaste, submitUpload, submitGithub, getSubmissionStatus } from '../api/submissions';
import Button from '../components/Button';
import Card from '../components/Card';

const STEP_SELECT = 'SELECT';
const STEP_INPUT = 'INPUT';
const STEP_PROGRESS = 'PROGRESS';

const NewReview = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(STEP_SELECT);
  const [source, setSource] = useState(null); // 'PASTE', 'UPLOAD', 'GITHUB'
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [newProjectName, setNewProjectName] = useState('');
  const [isCreatingProject, setIsCreatingProject] = useState(false);

  // Form inputs
  const [code, setCode] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [file, setFile] = useState(null);

  // Job Tracking
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);

  const { data: projects, refetch: refetchProjects } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const res = await getProjects();
      return res.data;
    }
  });

  const createProjectMutation = useMutation({
    mutationFn: createProject,
    onSuccess: (res) => {
      setSelectedProjectId(res.data.id);
      setIsCreatingProject(false);
      refetchProjects();
      toast.success('Project created!');
    }
  });

  const submitMutation = useMutation({
    mutationFn: async () => {
      const pid = selectedProjectId;
      if (source === 'PASTE') return submitPaste({ project_id: pid, code });
      if (source === 'GITHUB') return submitGithub({ project_id: pid, github_url: githubUrl });
      if (source === 'UPLOAD') {
        const formData = new FormData();
        formData.append('project_id', pid);
        formData.append('file', file);
        return submitUpload(formData);
      }
    },
    onSuccess: (res) => {
      setJobId(res.data.id || res.data.submission_id);
      setStep(STEP_PROGRESS);
      toast.success('Analysis started!');
    }
  });

  // Polling for Status
  useEffect(() => {
    let interval;
    if (step === STEP_PROGRESS && jobId) {
      interval = setInterval(async () => {
        try {
          const res = await getSubmissionStatus(jobId);
          setJobStatus(res.data);
          if (res.data.status === 'COMPLETED' || res.data.status === 'PARTIAL_SUCCESS') {
            clearInterval(interval);
            setTimeout(() => navigate(`/app/reviews/${res.data.review_id}`), 2000);
          } else if (res.data.status === 'FAILED') {
            clearInterval(interval);
            toast.error('Analysis failed.');
          }
        } catch (e) {
          console.error(e);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [step, jobId, navigate]);

  const handleSourceSelect = (src) => {
    setSource(src);
    setStep(STEP_INPUT);
  };

  const renderSelect = () => (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">New Code Review</h1>
        <p className="text-text-muted">Choose how you want to provide your code for analysis.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { id: 'PASTE', icon: Code2, label: 'Paste Code', desc: 'Copy-paste a single file or snippet.' },
          { id: 'UPLOAD', icon: Upload, label: 'Upload ZIP', desc: 'Upload a compressed Python project.' },
          { id: 'GITHUB', icon: Github, label: 'GitHub Repo', desc: 'Provide a public repository URL.' },
        ].map((item) => (
          <Card
            key={item.id}
            className="p-8 text-center hover:border-primary-main cursor-pointer transition-all flex flex-col items-center gap-4 group"
            onClick={() => handleSourceSelect(item.id)}
          >
            <div className="w-16 h-16 rounded-2xl bg-primary-soft flex items-center justify-center text-primary-main group-hover:scale-110 transition-transform">
              <item.icon size={32} />
            </div>
            <div>
              <h3 className="text-lg font-bold">{item.label}</h3>
              <p className="text-xs text-text-muted mt-1">{item.desc}</p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );

  const renderInput = () => (
    <div className="max-w-3xl mx-auto space-y-6">
      <Button variant="ghost" onClick={() => setStep(STEP_SELECT)} className="mb-4">
        ← Back to selection
      </Button>

      <Card className="p-8">
        <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
          {source === 'PASTE' && <Code2 />}
          {source === 'UPLOAD' && <Upload />}
          {source === 'GITHUB' && <Github />}
          Configure Submission
        </h2>

        <div className="space-y-6">
          {/* Project Selection */}
          <div>
            <label className="block text-sm font-semibold mb-2">Assign to Project</label>
            {!isCreatingProject ? (
              <div className="flex gap-2">
                <select
                  className="flex-1 p-2.5 bg-surface-app border border-surface-border rounded-2xl outline-none text-text-base"
                  value={selectedProjectId}
                  onChange={(e) => setSelectedProjectId(e.target.value)}
                >
                  <option value="">Select a project...</option>
                  {projects?.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                </select>
                <Button variant="secondary" onClick={() => setIsCreatingProject(true)}>
                  <Plus size={18} />
                </Button>
              </div>
            ) : (
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Project name"
                  className="flex-1 p-2.5 bg-surface-app border border-surface-border rounded-2xl outline-none text-text-base"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                />
                <Button
                  onClick={() => createProjectMutation.mutate({ name: newProjectName })}
                  isLoading={createProjectMutation.isPending}
                >
                  Save
                </Button>
                <Button variant="ghost" onClick={() => setIsCreatingProject(false)}>Cancel</Button>
              </div>
            )}
          </div>

          {/* Source Specific Inputs */}
          {source === 'PASTE' && (
            <div>
              <label className="block text-sm font-semibold mb-2">Python Code</label>
              <textarea
                className="w-full h-64 p-4 bg-surface-app border border-surface-border text-green-500 font-mono text-sm rounded-lg outline-none"
                placeholder="# Paste your code here..."
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
            </div>
          )}

          {source === 'GITHUB' && (
            <div>
              <label className="block text-sm font-semibold mb-2">Repository URL</label>
              <div className="relative">
                <Github className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                <input
                  type="url"
                  className="w-full pl-10 pr-4 py-2.5 bg-surface-app border border-surface-border rounded-2xl outline-none text-text-base"
                  placeholder="https://github.com/user/repo"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                />
              </div>
            </div>
          )}

          {source === 'UPLOAD' && (
            <div>
              <label className="block text-sm font-semibold mb-2">Project ZIP File</label>
              <div
                className="border-2 border-dashed border-surface-border rounded-[24px] p-12 text-center hover:border-primary-main transition-colors relative"
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                  e.preventDefault();
                  setFile(e.dataTransfer.files[0]);
                }}
              >
                <input
                  type="file"
                  accept=".zip"
                  className="absolute inset-0 opacity-0 cursor-pointer"
                  onChange={(e) => setFile(e.target.files[0])}
                />
                <Upload className="mx-auto text-slate-400 mb-4" size={32} />
                <p className="text-sm font-medium">{file ? file.name : "Click or drag ZIP file here"}</p>
                <p className="text-xs text-text-muted mt-1">Maximum size: 10MB</p>
              </div>
            </div>
          )}

          <Button
            className="w-full h-12 text-lg"
            disabled={!selectedProjectId || submitMutation.isPending}
            onClick={() => submitMutation.mutate()}
            isLoading={submitMutation.isPending}
          >
            Start Analysis <ArrowRight size={20} className="ml-2" />
          </Button>
        </div>
      </Card>
    </div>
  );

  const renderProgress = () => {
    const stages = [
      { id: 'QUEUED', label: 'Queued' },
      { id: 'VALIDATING', label: 'Validating' },
      { id: 'PREPARING_WORKSPACE', label: 'Preparing Workspace' },
      { id: 'DISCOVERING_FILES', label: 'Discovering Code' },
      { id: 'STATIC_ANALYSIS', label: 'Running Static Analysis' },
      { id: 'AI_ANALYSIS', label: 'Consulting AI Mentor' },
      { id: 'COMPLETED', label: 'Finished' },
    ];

    const currentIdx = stages.findIndex(s => s.id === jobStatus?.status);

    return (
      <div className="max-w-2xl mx-auto py-12 space-y-12">
        <div className="text-center space-y-4">
           {jobStatus?.status === 'FAILED' ? (
             <div className="w-20 h-20 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto">
                <AlertCircle size={48} />
             </div>
           ) : jobStatus?.status === 'COMPLETED' ? (
             <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto">
                <CheckCircle2 size={48} />
             </div>
           ) : (
             <div className="w-20 h-20 bg-primary-soft text-primary-main rounded-full flex items-center justify-center mx-auto">
                <Loader2 size={48} className="animate-spin" />
             </div>
           )}
           <h2 className="text-3xl font-bold">
             {jobStatus?.status === 'FAILED' ? 'Analysis Failed' : jobStatus?.status === 'COMPLETED' ? 'Analysis Complete' : 'Analyzing Code...'}
           </h2>
           <p className="text-text-muted italic">"A senior engineer is currently reviewing your project."</p>
        </div>

        <div className="space-y-6">
           {stages.map((stage, idx) => {
             const isPast = idx < currentIdx;
             const isCurrent = idx === currentIdx;

             return (
               <div key={stage.id} className="flex items-center gap-4">
                  <div className={`w-3 h-3 rounded-full ${isPast ? 'bg-green-500' : isCurrent ? 'bg-primary-main animate-pulse' : 'bg-surface-muted'}`} />
                  <span className={`text-sm font-medium ${isCurrent ? 'text-primary-main' : isPast ? 'text-text-base' : 'text-text-muted'}`}>
                    {stage.label}
                  </span>
                  {isPast && <CheckCircle2 size={14} className="text-green-500" />}
               </div>
             );
           })}
        </div>

        {jobStatus?.status === 'COMPLETED' && (
          <div className="text-center animate-bounce">
            <p className="text-sm font-bold text-primary-main">Redirecting to report...</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="pb-20">
      {step === STEP_SELECT && renderSelect()}
      {step === STEP_INPUT && renderInput()}
      {step === STEP_PROGRESS && renderProgress()}
    </div>
  );
};

export default NewReview;
