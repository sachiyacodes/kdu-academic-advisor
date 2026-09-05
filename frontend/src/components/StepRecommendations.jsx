import React, { useState, useMemo } from 'react';
import {
  Award,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Cpu,
  Brain,
  Sliders,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ArrowRight,
  ArrowLeft,
  TrendingUp,
} from 'lucide-react';

export default function StepRecommendations({
  recData,
  loading,
  onWeightChange,
  onPrev,
  onNext,
}) {
  const [expandedSpec, setExpandedSpec] = useState(null);
  const [academicWeight, setAcademicWeight] = useState(0.70);

  // Re-rank dynamically if user slides What-If weights locally
  const dynamicRankings = useMemo(() => {
    if (!recData || !recData.recommendations) return [];
    const interestWeight = 1.0 - academicWeight;

    const list = recData.recommendations.map((r) => {
      const recalculated = Number(
        (r.academic_fit * academicWeight + r.interest_alignment * interestWeight).toFixed(2)
      );
      return {
        ...r,
        dynamic_score: recalculated,
      };
    });

    list.sort((a, b) => b.dynamic_score - a.dynamic_score);
    return list;
  }, [recData, academicWeight]);

  if (loading) {
    return (
      <div className="py-24 text-center space-y-4 animate-fadeIn">
        <div className="w-12 h-12 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin mx-auto" />
        <h2 className="text-base font-bold text-white">Synthesizing Recommendations...</h2>
        <p className="text-xs text-slate-400 max-w-sm mx-auto">
          Executing academic fit scoring, content-based interest alignment, and machine learning cross-checks.
        </p>
      </div>
    );
  }

  if (!recData || !recData.recommendations || recData.recommendations.length === 0) {
    return (
      <div className="py-20 text-center space-y-4">
        <AlertCircle className="w-10 h-10 text-amber-400 mx-auto" />
        <h2 className="text-base font-bold text-white">No Data to Recommend</h2>
        <p className="text-xs text-slate-400 max-w-md mx-auto">
          Please add courses in Step 2 or load a demo profile to view personalized specialization guidance.
        </p>
        <button
          onClick={onPrev}
          className="text-xs bg-indigo-600 text-white px-4 py-2 rounded-xl font-semibold"
        >
          Go Back to Courses
        </button>
      </div>
    );
  }

  const topRec = dynamicRankings[0];
  const ml = recData.ml_crosscheck;

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 4 of 6 · Hybrid AI Recommender</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Specialization Recommendations
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Synthesized using multi-criteria weighted scoring (70% Academic Fit) and content-based matching (30% Interest Alignment), cross-checked by machine learning.
          </p>
        </div>

        {/* Top Recommendation Highlight Badge */}
        {topRec && (
          <div className="bg-gradient-to-r from-indigo-950/80 to-purple-950/80 border border-indigo-700/60 rounded-2xl p-3 px-5 shadow-xl flex items-center space-x-3">
            <Award className="w-8 h-8 text-amber-400" />
            <div>
              <span className="text-[10px] uppercase font-bold text-indigo-300 block tracking-wider">
                Top Compatible Pathway
              </span>
              <span className="text-base font-black text-white">
                {topRec.specialization_name}
              </span>
              <span className="text-xs text-indigo-300 ml-2 font-mono font-bold">
                ({topRec.dynamic_score}%)
              </span>
            </div>
          </div>
        )}
      </div>

      {/* What-If Sensitivity Slider */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-indigo-400" />
            <h3 className="text-xs font-bold text-white uppercase tracking-wider">
              Interactive What-If Sensitivity Analysis
            </h3>
          </div>
          <div className="text-xs font-semibold text-slate-300">
            Academic Fit: <span className="text-indigo-400 font-bold">{Math.round(academicWeight * 100)}%</span> · Interest: <span className="text-violet-400 font-bold">{Math.round((1 - academicWeight) * 100)}%</span>
          </div>
        </div>

        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={academicWeight}
          onChange={(e) => setAcademicWeight(parseFloat(e.target.value))}
          className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
        />

        <div className="flex justify-between text-[11px] text-slate-400">
          <span>🎯 Pure Interest (0% Academic / 100% Interest)</span>
          <span className="text-indigo-400 font-medium">Standard Hybrid Baseline (70/30)</span>
          <span>📚 Pure Grades (100% Academic / 0% Interest)</span>
        </div>
      </div>

      {/* Main Grid: Ranked Recommendations List + ML Cross-Check Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Ranked Specialization Cards */}
        <div className="lg:col-span-2 space-y-4">
          <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
            <Award className="w-4 h-4 text-indigo-400" />
            <span>Ranked Specialization Pathways</span>
          </h2>

          <div className="space-y-3">
            {dynamicRankings.map((r, index) => {
              const rank = index + 1;
              const isExpanded = expandedSpec === r.specialization_name;
              const explanation = recData.explanations?.[r.specialization_name];

              let evidenceColor = 'text-slate-400 bg-slate-800/60 border-slate-700';
              if (r.evidence_level === 'Strong Evidence') {
                evidenceColor = 'text-emerald-400 bg-emerald-950/40 border-emerald-800/50';
              } else if (r.evidence_level === 'Moderate Evidence') {
                evidenceColor = 'text-indigo-400 bg-indigo-950/40 border-indigo-800/50';
              } else if (r.evidence_level === 'Limited Evidence') {
                evidenceColor = 'text-amber-400 bg-amber-950/40 border-amber-800/50';
              }

              return (
                <div
                  key={r.specialization_name}
                  className={`bg-slate-900/70 border rounded-2xl p-4 shadow-sm transition ${
                    rank === 1
                      ? 'border-indigo-500/70 shadow-indigo-500/5 ring-1 ring-indigo-500/30'
                      : 'border-slate-800 hover:border-slate-700'
                  }`}
                >
                  {/* Card Header Row */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-center space-x-3">
                      <div className={`w-8 h-8 rounded-xl flex items-center justify-center font-black text-sm ${
                        rank === 1
                          ? 'bg-amber-400 text-slate-950 shadow-md shadow-amber-400/20'
                          : rank === 2
                          ? 'bg-slate-700 text-white'
                          : 'bg-slate-800 text-slate-400'
                      }`}>
                        #{rank}
                      </div>
                      <div>
                        <h3 className="text-sm font-bold text-white flex items-center space-x-2">
                          <span>{r.specialization_name}</span>
                          {rank === 1 && (
                            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-amber-400/10 text-amber-400 border border-amber-400/20">
                              Primary Fit
                            </span>
                          )}
                        </h3>
                        <div className="flex items-center space-x-2 mt-0.5">
                          <span className={`text-[10px] px-2 py-0.5 rounded-full border font-medium ${evidenceColor}`}>
                            {r.evidence_level}
                          </span>
                          <span className="text-[11px] text-slate-400">
                            {r.relevant_course_count} courses evaluated
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Scores Breakdown Badges */}
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                          Compatibility
                        </span>
                        <span className="text-xl font-black text-white">
                          {r.dynamic_score}
                          <span className="text-xs text-slate-500 font-normal"> / 100</span>
                        </span>
                      </div>

                      <div className="h-8 w-px bg-slate-800" />

                      <div className="text-right text-[11px]">
                        <div className="text-slate-400">
                          Academic: <strong className="text-indigo-400">{r.academic_fit.toFixed(1)}%</strong>
                        </div>
                        <div className="text-slate-400">
                          Interest: <strong className="text-violet-400">{r.interest_alignment.toFixed(1)}%</strong>
                        </div>
                      </div>

                      {/* Expand Button */}
                      <button
                        onClick={() => setExpandedSpec(isExpanded ? null : r.specialization_name)}
                        className="p-1.5 rounded-lg border border-slate-800 hover:border-slate-700 text-slate-400 hover:text-white"
                        title="Toggle XAI Explanation"
                      >
                        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  {/* Expandable Explainable AI (XAI) Drawer */}
                  {isExpanded && explanation && (
                    <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-4 text-xs animate-fadeIn">
                      {/* Summary */}
                      <div className="bg-slate-950/70 rounded-xl p-3 border border-slate-800/80 text-slate-300 leading-relaxed">
                        <strong className="text-indigo-400">Recommendation Rationale: </strong>
                        {explanation.summary}
                      </div>

                      {/* Strengths & Weaknesses */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div className="bg-slate-950/50 rounded-xl p-3 border border-slate-800/60 space-y-2">
                          <span className="text-emerald-400 font-bold flex items-center space-x-1.5">
                            <CheckCircle2 className="w-3.5 h-3.5" />
                            <span>Top Foundational Strengths</span>
                          </span>
                          <ul className="space-y-1 text-slate-300 list-disc list-inside">
                            {explanation.strengths.map((s, i) => (
                              <li key={i}>{s}</li>
                            ))}
                          </ul>
                        </div>

                        <div className="bg-slate-950/50 rounded-xl p-3 border border-slate-800/60 space-y-2">
                          <span className="text-amber-400 font-bold flex items-center space-x-1.5">
                            <AlertCircle className="w-3.5 h-3.5" />
                            <span>Areas for Improvement / Missing Data</span>
                          </span>
                          <ul className="space-y-1 text-slate-300 list-disc list-inside">
                            {explanation.weaknesses.map((w, i) => (
                              <li key={i}>{w}</li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      {/* Counterfactual Actionable Pathway */}
                      {explanation.counterfactuals && explanation.counterfactuals.length > 0 && (
                        <div className="bg-indigo-950/30 border border-indigo-700/40 rounded-xl p-3 text-indigo-200">
                          <strong className="text-indigo-300 block mb-1">
                            🚀 Actionable Pathway to Rank #1:
                          </strong>
                          {explanation.counterfactuals.map((cf, i) => (
                            <p key={i} className="leading-relaxed">{cf}</p>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Right 1 Col: Machine Learning Consensus Cross-Check */}
        <div className="space-y-4">
          <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
            <div className="flex items-center space-x-2 text-indigo-400 font-semibold text-sm">
              <Brain className="w-4 h-4" />
              <span>Machine Learning Cross-Check</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Trained Decision Tree & Random Forest classifiers evaluate transcript patterns independently from the rule-based weighted sum.
            </p>

            {ml ? (
              <div className="space-y-4 text-xs">
                {/* Consensus Indicator */}
                <div className={`p-3 rounded-xl border flex items-center justify-between ${
                  ml.consensus
                    ? 'bg-emerald-950/30 border-emerald-800/50 text-emerald-300'
                    : 'bg-indigo-950/30 border-indigo-800/50 text-indigo-300'
                }`}>
                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-400 block">
                      Ensemble ML Prediction
                    </span>
                    <strong className="text-white text-xs">{ml.prediction}</strong>
                  </div>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold border ${
                    ml.consensus
                      ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-400'
                      : 'bg-indigo-500/20 border-indigo-500/40 text-indigo-400'
                  }`}>
                    {ml.confidence_label}
                  </span>
                </div>

                {/* Probability Distribution */}
                <div className="space-y-2">
                  <span className="text-[11px] font-semibold text-slate-300 block">
                    Class Probability Distribution:
                  </span>
                  <div className="space-y-1.5">
                    {ml.probabilities && Object.entries(ml.probabilities).map(([label, prob]) => {
                      const pct = Math.round(prob * 100);
                      return (
                        <div key={label} className="space-y-0.5">
                          <div className="flex justify-between text-[11px] text-slate-400">
                            <span className="truncate pr-2">{label}</span>
                            <span className="font-mono text-slate-300 font-bold">{pct}%</span>
                          </div>
                          <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                            <div
                              className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full"
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {ml.is_preliminary && (
                  <p className="text-[11px] text-amber-400/90 bg-amber-950/20 border border-amber-800/30 rounded-lg p-2 leading-tight">
                    ⚠️ <em>Preliminary Confidence:</em> Fewer than 3 core areas evaluated. Predictions will sharpen as more courses are completed.
                  </p>
                )}
              </div>
            ) : (
              <p className="text-xs text-slate-500">
                Machine learning model currently unavailable.
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-slate-800 flex items-center justify-between">
        <button
          onClick={onPrev}
          className="flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-white px-4 py-2 rounded-xl hover:bg-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Interests</span>
        </button>

        <button
          onClick={onNext}
          className="flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-600/25 transition"
        >
          <span>View Elective Advisor & Roadmap</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
