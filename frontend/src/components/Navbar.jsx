import React from 'react';
import { GraduationCap, RotateCcw, Sparkles, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Navbar({
  currentStep,
  setCurrentStep,
  completedSteps,
  demoProfiles,
  onLoadDemo,
  onReset,
  backendOnline,
}) {
  const steps = [
    { id: 1, label: 'Profile' },
    { id: 2, label: 'Courses' },
    { id: 3, label: 'Interests' },
    { id: 4, label: 'Recommendations' },
    { id: 5, label: 'Elective Advisor' },
    { id: 6, label: 'Graduation Audit' },
  ];

  return (
    <header className="border-b border-slate-800 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setCurrentStep(1)}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg text-white tracking-tight">KDU Academic Advisor</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-medium">
                  AI Recommender
                </span>
              </div>
              <p className="text-xs text-slate-400">IT3182 Essentials of AI · Group 22</p>
            </div>
          </div>

          {/* Actions: Demo Profile Dropdown + Reset */}
          <div className="flex items-center space-x-3">
            {/* Backend status */}
            <div className="hidden md:flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs">
              <div className={`w-2 h-2 rounded-full ${backendOnline ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
              <span className="text-slate-400">{backendOnline ? 'API Connected' : 'Connecting...'}</span>
            </div>

            {/* Quick Demo Profiles */}
            <div className="relative inline-block">
              <select
                onChange={(e) => {
                  if (e.target.value) {
                    onLoadDemo(e.target.value);
                    e.target.value = '';
                  }
                }}
                defaultValue=""
                className="bg-indigo-950/60 hover:bg-indigo-900/60 border border-indigo-700/50 text-indigo-200 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer transition font-medium"
              >
                <option value="" disabled>✨ Load Demo Profile...</option>
                {demoProfiles && Object.entries(demoProfiles).map(([k, p]) => (
                  <option key={k} value={k} className="bg-slate-900 text-slate-200">
                    {p.title}
                  </option>
                ))}
              </select>
            </div>

            {/* Reset Button */}
            <button
              onClick={onReset}
              title="Reset profile and courses"
              className="p-1.5 rounded-lg border border-slate-800 hover:border-rose-500/40 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Step Navigation Bar */}
        <div className="flex items-center justify-between border-t border-slate-800/80 py-2.5 overflow-x-auto no-scrollbar">
          {steps.map((s) => {
            const isActive = currentStep === s.id;
            const isCompleted = completedSteps.includes(s.id);
            return (
              <button
                key={s.id}
                onClick={() => setCurrentStep(s.id)}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition whitespace-nowrap ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                    : isCompleted
                    ? 'text-emerald-400 hover:bg-slate-900'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/50'
                }`}
              >
                <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                  isActive
                    ? 'bg-white text-indigo-700'
                    : isCompleted
                    ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    : 'bg-slate-800 text-slate-400'
                }`}>
                  {isCompleted && !isActive ? '✓' : s.id}
                </span>
                <span>{s.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </header>
  );
}
