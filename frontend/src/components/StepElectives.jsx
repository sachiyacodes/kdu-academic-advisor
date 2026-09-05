import React, { useState } from 'react';
import {
  Compass,
  CheckCircle2,
  AlertCircle,
  Clock,
  Unlock,
  Layers,
  ArrowRight,
  ArrowLeft,
  Filter,
} from 'lucide-react';

export default function StepElectives({
  advisorData,
  loading,
  targetSpec,
  setTargetSpec,
  specializations,
  onPrev,
  onNext,
}) {
  const [activeTab, setActiveTab] = useState('electives'); // 'electives', 'cores', 'roadmap'

  if (loading) {
    return (
      <div className="py-24 text-center space-y-4 animate-fadeIn">
        <div className="w-12 h-12 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin mx-auto" />
        <h2 className="text-base font-bold text-white">Analyzing Prerequisite Graphs & Synergy...</h2>
        <p className="text-xs text-slate-400 max-w-sm mx-auto">
          Evaluating prerequisite fulfillment, stage eligibility, and career specialization synergy scores.
        </p>
      </div>
    );
  }

  if (!advisorData) {
    return (
      <div className="py-20 text-center space-y-4">
        <AlertCircle className="w-10 h-10 text-amber-400 mx-auto" />
        <h2 className="text-base font-bold text-white">No Advisor Data Available</h2>
        <button onClick={onPrev} className="text-xs bg-indigo-600 text-white px-4 py-2 rounded-xl font-semibold">
          Back to Recommendations
        </button>
      </div>
    );
  }

  const { electives = [], core_courses = [], roadmap = {} } = advisorData;

  const recNow = electives.filter((e) => e.category === 'Recommended Now');
  const recLater = electives.filter((e) => e.category === 'Recommended Later');
  const recLow = electives.filter((e) => e.category === 'Low Priority');

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 5 of 6 · Rule-Based Advisor</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Elective Advisor & Degree Roadmap
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Rule-based course eligibility and specialization synergy scoring to build your semester-by-semester plan.
          </p>
        </div>

        {/* Target Specialization Selector */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-3 px-4 shadow-lg space-y-1">
          <label className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
            Target Pathway for Synergy Scoring:
          </label>
          <select
            value={targetSpec}
            onChange={(e) => setTargetSpec(e.target.value)}
            className="bg-slate-950 border border-slate-700 text-xs text-indigo-300 font-semibold rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer"
          >
            {specializations && specializations.map((s) => (
              <option key={s.specialization_id} value={s.name}>
                {s.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-4">
        <button
          onClick={() => setActiveTab('electives')}
          className={`pb-3 text-xs font-bold transition border-b-2 flex items-center space-x-2 ${
            activeTab === 'electives'
              ? 'border-indigo-500 text-white'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Compass className="w-4 h-4" />
          <span>Personalized Elective Advisor ({electives.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('cores')}
          className={`pb-3 text-xs font-bold transition border-b-2 flex items-center space-x-2 ${
            activeTab === 'cores'
              ? 'border-indigo-500 text-white'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Layers className="w-4 h-4" />
          <span>Core Degree Pathways ({core_courses.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('roadmap')}
          className={`pb-3 text-xs font-bold transition border-b-2 flex items-center space-x-2 ${
            activeTab === 'roadmap'
              ? 'border-indigo-500 text-white'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Clock className="w-4 h-4" />
          <span>4-Year Curriculum Roadmap</span>
        </button>
      </div>

      {/* Tab 1: Electives */}
      {activeTab === 'electives' && (
        <div className="space-y-6">
          {/* Section: Recommended Now */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h2 className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>Recommended Now ({recNow.length}) — Prerequisites Met & Stage Eligible</span>
              </h2>
            </div>

            {recNow.length === 0 ? (
              <p className="text-xs text-slate-500 italic p-4 bg-slate-900/40 rounded-xl border border-slate-800">
                No electives currently eligible for immediate enrollment. Check prerequisites in Recommended Later below.
              </p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {recNow.map((item) => (
                  <div
                    key={item.course.course_code}
                    className="bg-slate-900/80 border border-emerald-900/40 rounded-2xl p-4 space-y-2.5 shadow-sm"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-xs font-bold text-emerald-400 font-mono">
                            {item.course.course_code}
                          </span>
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">
                            {item.course.credits} cr · Y{item.course.year} S{item.course.semester}
                          </span>
                        </div>
                        <h3 className="text-xs font-bold text-white mt-1">
                          {item.course.course_name}
                        </h3>
                        <p className="text-[11px] text-slate-400">{item.course.subject_area}</p>
                      </div>

                      <div className="text-right">
                        <span className="text-[10px] uppercase font-bold text-slate-400 block">
                          Synergy
                        </span>
                        <span className="text-base font-black text-indigo-400">
                          {item.synergy_score}%
                        </span>
                      </div>
                    </div>

                    <p className="text-xs text-slate-300 bg-slate-950/60 rounded-xl p-2.5 border border-slate-800/80 leading-relaxed">
                      {item.reason}
                    </p>

                    {item.chain_impact_count > 0 && (
                      <div className="text-[11px] text-amber-300 flex items-center space-x-1.5 font-medium">
                        <Unlock className="w-3.5 h-3.5" />
                        <span>Foundational: Unlocks {item.chain_impact_count} advanced course{item.chain_impact_count > 1 ? 's' : ''}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Section: Recommended Later */}
          <div className="space-y-3 pt-4">
            <h2 className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center space-x-2">
              <Clock className="w-4 h-4" />
              <span>Recommended Later ({recLater.length}) — Pending Prerequisites or Later Semester</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {recLater.slice(0, 10).map((item) => (
                <div
                  key={item.course.course_code}
                  className="bg-slate-900/60 border border-amber-950/40 rounded-2xl p-4 space-y-2.5 shadow-sm"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold text-amber-400 font-mono">
                          {item.course.course_code}
                        </span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">
                          {item.course.credits} cr · Y{item.course.year} S{item.course.semester}
                        </span>
                      </div>
                      <h3 className="text-xs font-bold text-white mt-1">
                        {item.course.course_name}
                      </h3>
                      <p className="text-[11px] text-slate-400">{item.course.subject_area}</p>
                    </div>

                    <div className="text-right">
                      <span className="text-[10px] uppercase font-bold text-slate-400 block">
                        Synergy
                      </span>
                      <span className="text-base font-black text-indigo-400">
                        {item.synergy_score}%
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-400 bg-slate-950/60 rounded-xl p-2.5 border border-slate-800/80 leading-relaxed">
                    {item.reason}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Core Courses */}
      {activeTab === 'cores' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {core_courses.map((item) => (
              <div
                key={item.course.course_code}
                className="bg-slate-900/70 border border-slate-800 rounded-xl p-3.5 space-y-2"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-xs font-mono font-bold text-indigo-400">
                      {item.course.course_code}
                    </span>
                    <h3 className="text-xs font-bold text-white mt-0.5">
                      {item.course.course_name}
                    </h3>
                  </div>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    item.category === 'Recommended Now'
                      ? 'bg-emerald-500/20 text-emerald-400'
                      : 'bg-slate-800 text-slate-400'
                  }`}>
                    {item.category}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400">{item.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Roadmap */}
      {activeTab === 'roadmap' && (
        <div className="space-y-6">
          {Object.entries(roadmap).map(([year, sems]) => (
            <div key={year} className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
              <h3 className="text-sm font-bold text-white border-b border-slate-800 pb-2">
                {year}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(sems).map(([sem, coursesList]) => (
                  <div key={sem} className="space-y-2">
                    <span className="text-xs font-semibold text-indigo-400 block">
                      {sem} ({coursesList.length} courses)
                    </span>
                    <div className="space-y-1.5">
                      {coursesList.map((c) => (
                        <div
                          key={c.course_code}
                          className="bg-slate-950/70 border border-slate-800/80 rounded-lg p-2 flex justify-between items-center text-xs"
                        >
                          <div>
                            <strong className="text-slate-200 font-mono">{c.course_code}</strong>
                            <span className="text-slate-400 ml-2">{c.course_name}</span>
                          </div>
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                            {c.credits} cr
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-slate-800 flex items-center justify-between">
        <button
          onClick={onPrev}
          className="flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-white px-4 py-2 rounded-xl hover:bg-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Recommendations</span>
        </button>

        <button
          onClick={onNext}
          className="flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-600/25 transition"
        >
          <span>View Graduation Audit</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
