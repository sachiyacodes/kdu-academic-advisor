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
  BookOpen,
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
          Back to Elective Advisor
        </button>
      </div>
    );
  }

  const {
    gpa,
    classification,
    core_credits = 0,
    elective_credits = 0,
    gpa_credits_earned = 0,
    gpa_target = 120,
    gpa_progress_pct = 0,
    ngpa_credits_earned = 0,
    ngpa_target = 14,
    ngpa_progress_pct = 0,
    total_credits_earned = 0,
    is_eligible = false,
    bottlenecks = [],
  } = auditData;

  const profile = recData?.profile;
  const subjectPerfs = profile?.subject_performances || [];

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
            Official evaluation against KDU graduation requirements: 120 GPA credits and 14 NGPA credits.
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

      {/* Academic Standing Summary Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            Academic Stage
          </span>
          <span className="text-sm font-bold text-white mt-1 block">
            {profile ? `Year ${profile.year}, Sem ${profile.semester}` : 'In Progress'}
          </span>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            Cumulative GPA
          </span>
          <span className="text-sm font-bold text-indigo-400 mt-1 block">
            {gpa ? gpa.toFixed(2) : '0.00'}
          </span>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            GPA Standing
          </span>
          <span className="text-sm font-bold text-emerald-400 mt-1 block truncate">
            {classification || 'First Class Honours'}
          </span>
        </div>

        <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4">
          <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            Total Credits Earned
          </span>
          <span className="text-sm font-bold text-white mt-1 block">
            {total_credits_earned || gpa_credits_earned + ngpa_credits_earned} cr
          </span>
        </div>
      </div>

      {/* Credit Gauges Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* GPA Credits Card */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-lg space-y-4">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-xs font-bold text-slate-200 block">
                Core & Elective GPA Credits
              </span>
              <p className="text-[11px] text-slate-400">
                Core: <strong className="text-slate-200">{core_credits}</strong> cr · Elective: <strong className="text-slate-200">{elective_credits}</strong> cr
              </p>
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
              <span className="text-xs font-bold text-slate-200 block">
                Non-GPA (NGPA) Credits
              </span>
              <p className="text-[11px] text-slate-400">
                Auxiliary modules (English, Internship, Leadership)
              </p>
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

      {/* Curriculum & Benchmark Explanatory Badges */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3 text-slate-400 leading-relaxed">
          <strong className="text-slate-200 block mb-0.5">📚 KDU Electives Policy:</strong>
          In the KDU computing curricula, electives begin in <strong>Year 3, Semester 2</strong> and continue into Year 4. All modules taken in Years 1 & 2 are Core degree requirements.
        </div>
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3 text-slate-400 leading-relaxed">
          <strong className="text-slate-200 block mb-0.5">✨ Benchmark Archetypes:</strong>
          Demo profiles contain 4 key specialized modules ({gpa_credits_earned} credits) to demonstrate AI scoring and prerequisite logic. You can record more courses in <strong>Step 2</strong>.
        </div>
      </div>

      {/* Prerequisite Bottlenecks Detector */}
      {bottlenecks.length > 0 ? (
        <div className="bg-amber-950/25 border border-amber-800/50 rounded-2xl p-5 space-y-3 shadow-md">
          <div className="flex items-center space-x-2 text-amber-400 font-bold text-xs uppercase tracking-wider">
            <AlertTriangle className="w-4 h-4" />
            <span>Critical Prerequisite Bottlenecks Detected</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            The following uncompleted courses are required prerequisites for multiple upcoming courses in your degree curriculum. Prioritize these to avoid academic progression delays:
          </p>
          <ul className="space-y-1.5 text-xs text-slate-300 list-disc list-inside">
            {bottlenecks.map((b, i) => (
              <li key={i} className="leading-relaxed">
                {b}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <div className="bg-emerald-950/20 border border-emerald-800/40 rounded-2xl p-4 flex items-center space-x-3 text-emerald-300 text-xs shadow-sm">
          <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
          <div>
            <strong className="block text-white font-semibold">No Prerequisite Bottlenecks:</strong>
            <span>All upstream prerequisites for your current curriculum stage are satisfied.</span>
          </div>
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
              Evaluated Areas: <strong className="text-indigo-400">{subjectPerfs.length}</strong>
            </span>
          </div>

          <div className="space-y-3 pt-2">
            {subjectPerfs.map((p) => {
              const mark = p.average_mark;
              let barColor = 'from-indigo-500 to-violet-500';
              if (mark >= 80) barColor = 'from-emerald-500 to-teal-500';
              else if (mark < 60) barColor = 'from-amber-500 to-rose-500';

              const courseCountText =
                p.course_count === 1 ? '1 course' : `${p.course_count} courses`;

              return (
                <div key={p.subject_area} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300 font-medium">{p.subject_area}</span>
                    <span className="font-mono text-slate-300 font-bold">
                      {mark.toFixed(1)}% <span className="text-slate-500 font-normal">({courseCountText})</span>
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
