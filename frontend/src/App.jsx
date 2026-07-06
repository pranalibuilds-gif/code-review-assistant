import { useState, useEffect } from 'react'

function App() {
  const [health, setHealth] = useState(null)

  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(err => console.error("Failed to fetch health:", err))
  }, [])

  return (
    <div className="min-h-screen bg-surface-app p-8 flex flex-col items-center justify-center font-sans text-text-base">
      <div className="bg-surface-card p-12 rounded-xl shadow-lg border border-surface-border max-w-2xl w-full text-center">
        <h1 className="text-4xl font-bold text-primary-main mb-4">
          CodeSage Skeleton
        </h1>
        <p className="text-text-muted text-lg mb-8">
          The engineering foundation for your AI-powered code reviewer is live.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="p-4 bg-primary-soft rounded-lg border border-primary-main/20">
            <h3 className="font-semibold text-primary-main">Frontend</h3>
            <p className="text-sm text-slate-600">Vite + React + Tailwind</p>
            <span className="mt-2 inline-block px-2 py-1 bg-status-success text-white text-xs rounded-full">
              Ready
            </span>
          </div>
          <div className="p-4 bg-slate-100 rounded-lg border border-slate-200">
            <h3 className="font-semibold text-slate-800">Backend</h3>
            <p className="text-sm text-slate-600">FastAPI + Uvicorn</p>
            <span className={`mt-2 inline-block px-2 py-1 text-xs rounded-full ${health ? 'bg-status-success text-white' : 'bg-status-warning text-white'}`}>
              {health ? 'Online' : 'Checking...'}
            </span>
          </div>
        </div>

        {health && (
          <div className="text-left bg-slate-50 p-4 rounded border border-slate-200 font-mono text-xs overflow-auto">
            <pre>{JSON.stringify(health, null, 2)}</pre>
          </div>
        )}
      </div>

      <p className="mt-8 text-text-muted text-sm">
        Phase 1: Project Skeleton — Validation in Progress
      </p>
    </div>
  )
}

export default App
