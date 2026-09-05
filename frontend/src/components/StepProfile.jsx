import React from 'react';
import { BookOpen, Calendar, Sparkles, ArrowRight, UserCheck, School } from 'lucide-react';

export default function StepProfile({
  profile,
  setProfile,
  degrees,
  demoProfiles,
  onLoadDemo,
  onNext,
}) {
  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Page Header */}
      <div className="border-b border-slate-800 pb-5">
        <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
          <span>Step 1 of 6</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Academic Profile Setup
        </h1>
        <p className="text-sm text-slate-400 mt-1 max-w-3xl">
          Select your degree program and academic standing. You can also load one of the 6 benchmark demo profiles to immediately test the recommendation pipeline.
        </p>
      </div>

      {/* Main Form & Demo Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Form */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
            <h2 className="text-base font-semibold text-white flex items-center space-x-2">
              <School className="w-5 h-5 text-indigo-400" />
              <span>Degree & Curriculum</span>
            </h2>

            {/* Degree Select */}
            <div className="space-y-2">
              <label className="block text-xs font-medium text-slate-300">
                Enrolled Degree Program
              </label>
              <select
                value={profile.degree}
                onChange={(e) => setProfile({ ...profile, degree: e.target.value })}
                className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
              >
                {degrees.map((d) => (
                  <option key={d.degree_id} value={d.degree_name}>
                    {d.degree_name} ({d.department})
                  </option>
                ))}
              </select>
              {profile.degree === 'Custom / Other University Degree' && (
                <p className="text-xs text-amber-400 bg-amber-950/30 border border-amber-800/40 rounded-lg p-2.5 mt-2">
                  💡 <strong>Universal Curriculum Mode:</strong> Enables manual course entry from any institution and grants access to explore 89 electives across all computing departments.
                </p>
              )}
            </div>

            {/* Year & Semester */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="block text-xs font-medium text-slate-300 flex items-center space-x-1.5">
                  <Calendar className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Current Academic Year</span>
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {[1, 2, 3, 4].map((y) => (
                    <button
                      key={y}
                      type="button"
                      onClick={() => setProfile({ ...profile, year: y })}
                      className={`py-2.5 rounded-xl text-xs font-semibold transition ${
                        profile.year === y
                          ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                          : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
                      }`}
                    >
                      Year {y}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="block text-xs font-medium text-slate-300 flex items-center space-x-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Current Semester</span>
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {[1, 2].map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => setProfile({ ...profile, semester: s })}
                      className={`py-2.5 rounded-xl text-xs font-semibold transition ${
                        profile.semester === s
                          ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                          : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
                      }`}
                    >
                      Semester {s}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Next Button */}
            <div className="pt-4 flex justify-end">
              <button
                onClick={onNext}
                className="flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-sm font-semibold px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-600/25 transition"
              >
                <span>Proceed to Course History</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Right 1 Col: Benchmark Archetypes */}
        <div className="space-y-4">
          <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
            <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-sm">
              <Sparkles className="w-4 h-4" />
              <span>Benchmark Archetypes</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Click any profile to load pre-configured courses, marks, and interests for live demonstration:
            </p>

            <div className="space-y-2.5">
              {demoProfiles && Object.entries(demoProfiles).map(([key, demo]) => (
                <button
                  key={key}
                  onClick={() => onLoadDemo(key)}
                  className="w-full text-left p-3 rounded-xl bg-slate-950/60 hover:bg-indigo-950/40 border border-slate-800/80 hover:border-indigo-700/50 transition group"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200 group-hover:text-indigo-300">
                      {demo.title.split('—')[0].trim()}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 group-hover:bg-indigo-600 group-hover:text-white transition">
                      Load
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-1 line-clamp-2 leading-tight">
                    {demo.description}
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
