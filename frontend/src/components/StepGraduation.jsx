import React from 'react';
import {
  GraduationCap,
  Award,
  CheckCircle2,
  AlertTriangle,
  BarChart3,
  ArrowLeft,
  RotateCcw,
  Sparkles,
} from 'lucide-react';

export default function StepGraduation({
  auditData,
  recData,
  loading,
  onPrev,
  onReset,
}) {
  if (loading) {
    return (
      <div className="py-24 text-center space-y-4 animate-fadeIn">
        <div className="w-12 h-12 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin mx-auto" />
        <h2 className="text-base font-bold text-white">Running Graduation Credit Audit...</h2>
      </div>
    );
  }

  if (!auditData) {
    return (
      <div className="py-20 text-center space-y-4">
        <AlertTriangle className="w-10 h-10 text-amber-400 mx-auto" />
        <h2 className="text-base font-bold text-white">No Audit Data</h2>
        <button onClick={onPrev} className="text-xs bg-indigo-600 text-white px-4 py-2 rounded-xl font-semibold">
          Back to Electives
        </button>
      </div>
    );
  }

  const {
    gpa,
    gpa_credits_earned,
    gpa_target,
    gpa_progress_pct,
    ngpa_credits_earned,
    ngpa_target,
    ngpa_progress_pct,
    is_eligible,
    bottlenecks = [],
  } = auditData;

  const subjectPerfs = recData?.profile?.subject_performances || [];

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 6 of 6 · Degree Completion</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Graduation Credit Audit & Analytics
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Verification against KDU graduation requirements: 120 GPA credits and 14 NGPA credits.
          </p>
        </div>

        {/* Eligibility Banner */}
        <div className={`flex items-center space-x-3 px-5 py-3 rounded-2xl border shadow-lg ${
          is_eligible
            ? 'bg-emerald-950/40 border-emerald-800/60 text-emerald-300'
            : 'bg-indigo-950/40 border-indigo-800/60 text-indigo-300'
        }`}>
          <GraduationCap className={`w-8 h-8 ${is_eligible ? 'text-emerald-400' : 'text-indigo-400'}`} />
          <div>
            <span className="text-[10px] uppercase font-bold tracking-wider block">
              Graduation Clearance
            </span>
            <strong className="text-sm text-white font-bold">
              {is_eligible ? 'All Credit Targets Met 🎉' : 'Degree In Progress'}
            </strong>
          </div>
        </div>
      </div>

      {/* Credit Gauges Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* GPA Credits Card */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-xs font-bold text-slate-300 block">
                Core & Elective GPA Credits
              </span>
              <p className="text-[11px] text-slate-500">Minimum threshold: 120 credits</p>
            </div>
            <div className="text-right">
              <span className="text-2xl font-black text-white">{gpa_credits_earned}</span>
              <span className="text-xs text-slate-500 font-bold"> / {gpa_target}</span>
            </div>
          </div>

          <div className="space-y-1.5">
            <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full transition-all duration-500"
                style={{ width: `${gpa_progress_pct}%` }}
              />
            </div>
            <div className="flex justify-between text-[11px] text-slate-400 font-medium">
              <span>{gpa_progress_pct}% Complete</span>
              <span>{Math.max(0, gpa_target - gpa_credits_earned)} credits remaining</span>
            </div>
          </div>
        </div>

        {/* NGPA Credits Card */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-xs font-bold text-slate-300 block">
                Non-GPA (NGPA) Credits
              </span>
              <p className="text-[11px] text-slate-500">Compulsory auxiliary threshold: 14 credits</p>
            </div>
            <div className="text-right">
              <span className="text-2xl font-black text-white">{ngpa_credits_earned}</span>
              <span className="text-xs text-slate-500 font-bold"> / {ngpa_target}</span>
            </div>
          </div>

          <div className="space-y-1.5">
            <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full transition-all duration-500"
                style={{ width: `${ngpa_progress_pct}%` }}
              />
            </div>
            <div className="flex justify-between text-[11px] text-slate-400 font-medium">
              <span>{ngpa_progress_pct}% Complete</span>
              <span>{Math.max(0, ngpa_target - ngpa_credits_earned)} credits remaining</span>
            </div>
          </div>
        </div>
      </div>

      {/* Bottlenecks Detector */}
      {bottlenecks.length > 0 && (
        <div className="bg-amber-950/20 border border-amber-800/40 rounded-2xl p-5 space-y-2.5">
          <div className="flex items-center space-x-2 text-amber-400 font-bold text-xs">
            <AlertTriangle className="w-4 h-4" />
            <span>Curriculum Standing & Bottleneck Detector</span>
          </div>
          <ul className="space-y-1 text-xs text-slate-300 list-disc list-inside">
            {bottlenecks.map((b, i) => (
              <li key={i}>{b}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Subject Area Performance Chart / Distribution */}
      {subjectPerfs.length > 0 && (
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <BarChart3 className="w-4 h-4 text-indigo-400" />
              <span>Academic Performance by Subject Area</span>
            </h3>
            <span className="text-xs text-slate-400 font-medium">
              Cumulative GPA: <strong className="text-indigo-400">{gpa.toFixed(2)}</strong>
            </span>
          </div>

          <div className="space-y-3 pt-2">
            {subjectPerfs.map((p) => {
              const mark = p.average_mark;
              let barColor = 'from-indigo-500 to-violet-500';
              if (mark >= 80) barColor = 'from-emerald-500 to-teal-500';
              else if (mark < 60) barColor = 'from-amber-500 to-rose-500';

              return (
                <div key={p.subject_area} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-medium">{p.subject_area}</span>
                    <span className="font-mono text-slate-300 font-bold">
                      {mark.toFixed(1)}% <span className="text-slate-500 font-normal">({p.course_count} courses)</span>
                    </span>
                  </div>
                  <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full bg-gradient-to-r ${barColor} rounded-full transition-all duration-500`}
                      style={{ width: `${Math.min(100, mark)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Footer Controls */}
      <div className="pt-6 border-t border-slate-800 flex items-center justify-between">
        <button
          onClick={onPrev}
          className="flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-white px-4 py-2 rounded-xl hover:bg-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Elective Advisor</span>
        </button>

        <button
          onClick={onReset}
          className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-5 py-2.5 rounded-xl transition"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Reset & Start New Evaluation</span>
        </button>
      </div>
    </div>
  );
}
