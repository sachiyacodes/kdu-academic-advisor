import React, { useState, useMemo } from 'react';
import {
  Award,
  ChevronDown,
  ChevronUp,
  Brain,
  Sliders,
  Check,
  AlertCircle,
  ArrowRight,
  ArrowLeft,
  Info,
  TrendingUp,
} from 'lucide-react';
import { Card, Button, Badge, Skeleton } from './ui';

export default function StepRecommendations({
  recData,
  loading,
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
      <div className="space-y-6 md:space-y-8 animate-fadeIn">
        <div className="border-b border-border pb-5 space-y-2">
          <Skeleton className="h-4 w-28" />
          <Skeleton className="h-8 w-80" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-4">
            <Skeleton className="h-36 w-full" />
            <Skeleton className="h-28 w-full" />
            <Skeleton className="h-28 w-full" />
          </div>
          <div>
            <Skeleton className="h-80 w-full" />
          </div>
        </div>
      </div>
    );
  }

  if (!recData || !recData.recommendations || recData.recommendations.length === 0) {
    return (
      <Card className="py-16 text-center space-y-4 max-w-lg mx-auto">
        <AlertCircle className="w-10 h-10 text-warning mx-auto" />
        <h2 className="text-base font-semibold text-text-primary">No Course Data Available</h2>
        <p className="text-xs text-text-secondary max-w-sm mx-auto leading-relaxed">
          Please add courses in Step 2 or load a student archetype to view algorithmic specialization guidance.
        </p>
        <Button
          variant="primary"
          size="md"
          onClick={onPrev}
        >
          Return to Course History
        </Button>
      </Card>
    );
  }

  const topRec = dynamicRankings[0];
  const ml = recData.ml_crosscheck;

  return (
    <div className="space-y-6 md:space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-border pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-primary text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 4 of 6 · Hybrid AI Recommender</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-primary tracking-tight">
            Specialization Recommendations
          </h1>
          <p className="text-sm text-text-secondary mt-1 max-w-3xl leading-relaxed">
            Multi-criteria weighted scoring ({Math.round(academicWeight * 100)}% Academic Fit) and content-based matching ({Math.round((1 - academicWeight) * 100)}% Career Interest), verified by ML classifiers.
          </p>
        </div>

        {/* Top Recommendation Highlight Pill */}
        {topRec && (
          <Card padding="sm" className="border-l-4 border-l-primary flex items-center space-x-3 px-4 shrink-0 shadow-xs">
            <Award className="w-6 h-6 text-primary shrink-0" />
            <div>
              <span className="text-[10px] uppercase font-bold text-text-secondary block tracking-wider">
                Top Compatible Pathway
              </span>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-bold text-text-primary">
                  {topRec.specialization_name}
                </span>
                <Badge variant="primary" size="sm">
                  {topRec.dynamic_score}%
                </Badge>
              </div>
            </div>
          </Card>
        )}
      </div>

      {/* Interactive Sensitivity Analysis Slider */}
      <Card padding="normal" className="space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-primary" />
            <h3 className="text-xs font-semibold text-text-primary uppercase tracking-wider">
              Sensitivity Analysis Calibration
            </h3>
          </div>
          <div className="text-xs font-medium text-text-secondary">
            Academic Fit: <strong className="text-primary font-semibold">{Math.round(academicWeight * 100)}%</strong> · Career Interest: <strong className="text-teal font-semibold">{Math.round((1 - academicWeight) * 100)}%</strong>
          </div>
        </div>

        <input
          type="range"
          min="0"
          max="1"
          step="0.05"
          value={academicWeight}
          aria-label="Adjust academic fit vs career interest weighting"
          onChange={(e) => setAcademicWeight(parseFloat(e.target.value))}
          className="w-full h-1.5 bg-border rounded-full appearance-none cursor-pointer focus-ring accent-primary"
          style={{
            background: `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${academicWeight * 100}%, var(--color-border) ${academicWeight * 100}%, var(--color-border) 100%)`,
          }}
        />

        <div className="flex justify-between text-[11px] text-text-muted">
          <span>Pure Interest (0% Grades)</span>
          <span className="text-primary font-medium">Standard Hybrid Fit (70/30)</span>
          <span>Pure Academic Fit (100% Grades)</span>
        </div>
      </Card>

      {/* Main Grid: Ranked Recommendations List + ML Cross-Check Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
        {/* Left 2 Cols: Ranked Specialization Cards */}
        <div className="lg:col-span-2 space-y-3.5">
          <h2 className="text-sm font-semibold text-text-primary flex items-center space-x-2">
            <Award className="w-4 h-4 text-primary" />
            <span>Ranked Specialization Pathways</span>
          </h2>

          <div className="space-y-3">
            {dynamicRankings.map((r, index) => {
              const rank = index + 1;
              const isExpanded = expandedSpec === r.specialization_name;
              const explanation = recData.explanations?.[r.specialization_name];

              let evidenceVariant = 'neutral';
              if (r.evidence_level === 'Strong Evidence') evidenceVariant = 'success';
              else if (r.evidence_level === 'Moderate Evidence') evidenceVariant = 'primary';
              else if (r.evidence_level === 'Limited Evidence') evidenceVariant = 'warning';

              return (
                <Card
                  key={r.specialization_name}
                  className={`transition-all duration-150 ${
                    rank === 1
                      ? 'border-l-4 border-l-primary bg-surface shadow-xs'
                      : 'hover:border-border'
                  }`}
                >
                  {/* Card Header Row */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-center space-x-3.5">
                      <div
                        className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                          rank === 1
                            ? 'bg-primary text-white shadow-xs'
                            : 'bg-surface-elevated text-text-secondary border border-border'
                        }`}
                      >
                        #{rank}
                      </div>
                      <div>
                        <div className="flex items-center space-x-2">
                          <h3 className="text-sm font-semibold text-text-primary">
                            {r.specialization_name}
                          </h3>
                          {rank === 1 && (
                            <Badge variant="primary" size="sm">
                              Primary Fit
                            </Badge>
                          )}
                        </div>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge variant={evidenceVariant} size="sm">
                            {r.evidence_level}
                          </Badge>
                          <span className="text-[11px] text-text-muted">
                            {r.relevant_course_count} courses evaluated
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Scores Breakdown Badges & Expand Trigger */}
                    <div className="flex items-center space-x-4 self-end sm:self-auto">
                      <div className="text-right">
                        <span className="text-[10px] text-text-muted uppercase tracking-wider block font-medium">
                          Compatibility
                        </span>
                        <span className="text-xl font-black text-text-primary">
                          {r.dynamic_score}
                          <span className="text-xs text-text-muted font-normal"> / 100</span>
                        </span>
                      </div>

                      <div className="h-8 w-px bg-border-subtle" />

                      <div className="text-right text-[11px] space-y-0.5">
                        <div className="text-text-secondary">
                          Academic: <strong className="text-primary font-semibold">{r.academic_fit.toFixed(1)}%</strong>
                        </div>
                        <div className="text-text-secondary">
                          Interest: <strong className="text-teal font-semibold">{r.interest_alignment.toFixed(1)}%</strong>
                        </div>
                      </div>

                      {/* Expand Button */}
                      <button
                        type="button"
                        onClick={() => setExpandedSpec(isExpanded ? null : r.specialization_name)}
                        className="p-1.5 rounded-lg border border-border hover:bg-surface-hover text-text-secondary hover:text-text-primary transition-colors cursor-pointer focus-ring"
                        title="Toggle XAI Explanation"
                        aria-expanded={isExpanded}
                      >
                        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  {/* Expandable Explainable AI (XAI) Drawer */}
                  {isExpanded && explanation && (
                    <div className="mt-4 pt-4 border-t border-border-subtle space-y-3.5 text-xs animate-fadeIn">
                      {/* Summary Rationale */}
                      <div className="bg-bg-secondary rounded-lg p-3 border border-border text-text-primary leading-relaxed">
                        <strong className="text-primary">Recommendation Rationale: </strong>
                        {explanation.summary}
                      </div>

                      {/* Strengths & Growth Areas */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <div className="bg-bg-secondary/60 rounded-lg p-3 border border-border space-y-2">
                          <span className="text-success font-semibold flex items-center space-x-1.5">
                            <Check className="w-3.5 h-3.5" />
                            <span>Foundational Strengths</span>
                          </span>
                          <ul className="space-y-1 text-text-secondary list-disc list-inside">
                            {explanation.strengths.map((s, i) => (
                              <li key={i}>{s}</li>
                            ))}
                          </ul>
                        </div>

                        <div className="bg-bg-secondary/60 rounded-lg p-3 border border-border space-y-2">
                          <span className="text-warning font-semibold flex items-center space-x-1.5">
                            <AlertCircle className="w-3.5 h-3.5" />
                            <span>Growth Areas / Missing Courses</span>
                          </span>
                          <ul className="space-y-1 text-text-secondary list-disc list-inside">
                            {explanation.weaknesses.map((w, i) => (
                              <li key={i}>{w}</li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      {/* Counterfactual Actionable Pathway */}
                      {explanation.counterfactuals && explanation.counterfactuals.length > 0 && (
                        <div className="bg-primary-subtle border border-primary-border rounded-lg p-3 text-text-primary">
                          <strong className="text-primary flex items-center space-x-1.5 mb-1">
                            <TrendingUp className="w-3.5 h-3.5" />
                            <span>Actionable Pathway to Maximize Standing:</span>
                          </strong>
                          {explanation.counterfactuals.map((cf, i) => (
                            <p key={i} className="text-xs text-text-secondary leading-relaxed mt-0.5">{cf}</p>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </Card>
              );
            })}
          </div>
        </div>

        {/* Right 1 Col: Dedicated Intelligence Teal ML Cross-Check Panel */}
        <div className="space-y-4">
          <Card variant="teal" className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-teal-border/30">
              <div className="flex items-center space-x-2 text-teal font-semibold text-xs tracking-wider uppercase">
                <Brain className="w-4 h-4" />
                <span>AI ML Cross-Check</span>
              </div>
              <Badge variant="teal" size="sm">
                Random Forest
              </Badge>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              Supervised machine learning models independently evaluate transcript patterns separate from rule-based calculations.
            </p>

            {ml ? (
              <div className="space-y-4 text-xs">
                {/* Prediction Consensus Box */}
                <div className="p-3.5 rounded-lg border border-teal-border/40 bg-teal-subtle flex items-center justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-semibold text-text-secondary block">
                      ML Predicted Specialization
                    </span>
                    <strong className="text-text-primary text-xs font-bold">{ml.prediction}</strong>
                  </div>
                  <Badge variant={ml.consensus ? 'success' : 'teal'} size="sm">
                    {ml.confidence_label}
                  </Badge>
                </div>

                {/* Probability Distribution */}
                <div className="space-y-2.5">
                  <span className="text-[11px] font-semibold text-text-primary block">
                    Class Probability Distribution:
                  </span>
                  <div className="space-y-2">
                    {ml.probabilities &&
                      Object.entries(ml.probabilities).map(([label, prob]) => {
                        const pct = Math.round(prob * 100);
                        return (
                          <div key={label} className="space-y-1">
                            <div className="flex justify-between text-[11px] text-text-secondary">
                              <span className="truncate pr-2">{label}</span>
                              <span className="font-mono text-text-primary font-semibold">{pct}%</span>
                            </div>
                            <div className="w-full h-1.5 bg-border rounded-full overflow-hidden">
                              <div
                                className="h-full bg-teal rounded-full transition-all duration-300"
                                style={{ width: `${pct}%` }}
                              />
                            </div>
                          </div>
                        );
                      })}
                  </div>
                </div>

                {/* Preliminary Alert */}
                {ml.is_preliminary && (
                  <div className="text-[11px] text-warning bg-warning-subtle border border-warning-border rounded-lg p-2.5 leading-relaxed flex items-start space-x-1.5">
                    <Info className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                    <span>
                      <strong>Preliminary ML Confidence:</strong> Fewer than 3 core areas evaluated. Prediction precision increases with subsequent completed courses.
                    </span>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-xs text-text-muted">
                Machine learning model inference pending or unavailable.
              </p>
            )}
          </Card>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-border flex items-center justify-between">
        <Button
          variant="secondary"
          size="md"
          icon={ArrowLeft}
          onClick={onPrev}
        >
          Back to Interests
        </Button>

        <Button
          variant="primary"
          size="lg"
          icon={ArrowRight}
          iconPosition="right"
          onClick={onNext}
        >
          View Elective Advisor & Roadmap
        </Button>
      </div>
    </div>
  );
}
