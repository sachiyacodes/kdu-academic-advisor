import React, { useState, useMemo } from 'react';
import {
  Award, ChevronDown, ChevronUp, Brain, Check,
  AlertCircle, ArrowRight, ArrowLeft, Info, TrendingUp,
} from 'lucide-react';
import { Button, Badge, Skeleton } from './ui';

export default function StepRecommendations({ recData, loading, onPrev, onNext }) {
  const [expandedSpec, setExpandedSpec] = useState(null);
  const [academicWeight, setAcademicWeight] = useState(0.70);

  const dynamicRankings = useMemo(() => {
    if (!recData?.recommendations) return [];
    const iw = 1.0 - academicWeight;
    return [...recData.recommendations]
      .map((r) => ({ ...r, dynamic_score: Number((r.academic_fit * academicWeight + r.interest_alignment * iw).toFixed(2)) }))
      .sort((a, b) => b.dynamic_score - a.dynamic_score);
  }, [recData, academicWeight]);

  if (loading) {
    return (
      <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>
        <div style={{ padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)', marginBottom: '24px' }}>
          <Skeleton className="h-4 w-28 mb-2" />
          <Skeleton className="h-7 w-72" />
          <Skeleton className="h-4 w-96 mt-2" />
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: '24px' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <Skeleton className="h-28 w-full" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
          </div>
          <Skeleton className="h-72 w-full" />
        </div>
      </div>
    );
  }

  if (!recData?.recommendations?.length) {
    return (
      <div style={{ maxWidth: '480px', margin: '64px auto', textAlign: 'center', padding: '0 16px' }}>
        <AlertCircle style={{ width: '32px', height: '32px', color: 'var(--color-warning)', margin: '0 auto 16px' }} />
        <h2 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--color-text-primary)', margin: '0 0 8px' }}>No data available</h2>
        <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: '0 0 20px', lineHeight: 1.6 }}>
          Add courses in Step 2 or load a student archetype to generate specialization recommendations.
        </p>
        <Button variant="primary" size="md" onClick={onPrev}>Return to course history</Button>
      </div>
    );
  }

  const topRec = dynamicRankings[0];
  const ml = recData.ml_crosscheck;
  const aw = Math.round(academicWeight * 100);
  const iw = 100 - aw;

  return (
    <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>

      {/* ── Header ───────────────────────────────────────────────── */}
      <div style={{
        padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '24px',
      }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <h1 style={{ fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em', color: 'var(--color-text-primary)', margin: 0, lineHeight: 1.3 }}>
            Specialization Recommendations
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: '6px 0 0', lineHeight: 1.6 }}>
            Hybrid scoring — {aw}% academic fit, {iw}% career interest — verified by ML classifiers.
          </p>
        </div>

        {/* Top pick callout */}
        {topRec && (
          <div style={{
            display: 'flex', alignItems: 'center', gap: '10px',
            background: 'var(--color-surface)', border: '1px solid var(--color-border)',
            borderLeft: '3px solid var(--color-primary)',
            borderRadius: '0 10px 10px 0', padding: '10px 14px', flexShrink: 0,
          }}>
            <Award style={{ width: '18px', height: '18px', color: 'var(--color-primary)', flexShrink: 0 }} />
            <div>
              <div style={{ fontSize: '10px', color: 'var(--color-text-muted)', fontWeight: 600, letterSpacing: '0.04em', marginBottom: '2px' }}>TOP MATCH</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-primary)' }}>{topRec.specialization_name}</span>
                <Badge variant="primary" size="sm">{topRec.dynamic_score}%</Badge>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Sensitivity slider ───────────────────────────────────── */}
      <div style={{
        background: 'var(--color-surface)', border: '1px solid var(--color-border)',
        borderRadius: '10px', padding: '16px 18px', margin: '20px 0',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>
            Weighting — what matters more to you?
          </span>
          <div style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>
            Academic <strong style={{ color: 'var(--color-primary)' }}>{aw}%</strong>
            &nbsp;·&nbsp;
            Interest <strong style={{ color: 'var(--color-teal)' }}>{iw}%</strong>
          </div>
        </div>
        <input
          type="range" min="0" max="1" step="0.05" value={academicWeight}
          aria-label="Adjust academic vs interest weighting"
          onChange={(e) => setAcademicWeight(parseFloat(e.target.value))}
          className="sensitivity-slider"
          style={{
            background: `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${academicWeight * 100}%, var(--color-border) ${academicWeight * 100}%, var(--color-border) 100%)`,
          }}
        />
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '8px' }}>
          <span>Pure career interest</span>
          <span style={{ color: 'var(--color-text-secondary)', fontWeight: 500 }}>Standard 70/30</span>
          <span>Pure academic fit</span>
        </div>
      </div>

      {/* ── Main grid ────────────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 272px', gap: '24px' }} className="recs-grid">

        {/* Left: ranked list */}
        <div>
          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.04em', marginBottom: '10px', textTransform: 'uppercase' }}>
            Ranked pathways
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {dynamicRankings.map((r, index) => {
              const rank = index + 1;
              const isTop = rank === 1;
              const isExpanded = expandedSpec === r.specialization_name;
              const explanation = recData.explanations?.[r.specialization_name];

              let evVariant = 'neutral';
              if (r.evidence_level === 'Strong Evidence') evVariant = 'success';
              else if (r.evidence_level === 'Moderate Evidence') evVariant = 'primary';
              else if (r.evidence_level === 'Limited Evidence') evVariant = 'warning';

              const scorePct = Math.round(r.dynamic_score);
              const barPct = Math.min(100, scorePct);

              return (
                <div
                  key={r.specialization_name}
                  style={{
                    background: 'var(--color-surface)', border: '1px solid var(--color-border)',
                    borderLeft: isTop ? '3px solid var(--color-primary)' : '1px solid var(--color-border)',
                    borderRadius: isTop ? '0 10px 10px 0' : '10px',
                    overflow: 'hidden', transition: 'border-color 120ms ease',
                  }}
                >
                  {/* Main row */}
                  <div style={{ padding: '14px 16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {/* Rank number */}
                    <div style={{
                      width: '24px', height: '24px', borderRadius: '50%', flexShrink: 0,
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: '11px', fontWeight: 700,
                      background: isTop ? 'var(--color-primary)' : 'var(--color-surface-elevated)',
                      color: isTop ? '#fff' : 'var(--color-text-muted)',
                      border: isTop ? 'none' : '1px solid var(--color-border)',
                    }}>
                      {rank}
                    </div>

                    {/* Name + score bar */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px', flexWrap: 'wrap' }}>
                        <span style={{ fontSize: '13px', fontWeight: isTop ? 700 : 600, color: 'var(--color-text-primary)' }}>
                          {r.specialization_name}
                        </span>
                        {isTop && <Badge variant="primary" size="sm">Primary fit</Badge>}
                        <Badge variant={evVariant} size="sm">{r.evidence_level}</Badge>
                      </div>
                      {/* Score bar */}
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ flex: 1, height: '3px', background: 'var(--color-border)', borderRadius: '2px', overflow: 'hidden' }}>
                          <div style={{ width: `${barPct}%`, height: '100%', background: isTop ? 'var(--color-primary)' : 'var(--color-text-muted)', borderRadius: '2px', transition: 'width 600ms cubic-bezier(0.25,1,0.5,1)' }} />
                        </div>
                        <span style={{ fontSize: '12px', fontWeight: 700, color: isTop ? 'var(--color-primary)' : 'var(--color-text-secondary)', fontVariantNumeric: 'tabular-nums', minWidth: '32px', textAlign: 'right' }}>
                          {scorePct}%
                        </span>
                      </div>
                    </div>

                    {/* Sub-scores */}
                    <div style={{ fontSize: '11px', textAlign: 'right', flexShrink: 0 }}>
                      <div style={{ color: 'var(--color-text-muted)', marginBottom: '2px' }}>
                        Acad <strong style={{ color: 'var(--color-primary)' }}>{r.academic_fit.toFixed(1)}%</strong>
                      </div>
                      <div style={{ color: 'var(--color-text-muted)' }}>
                        Int <strong style={{ color: 'var(--color-teal)' }}>{r.interest_alignment.toFixed(1)}%</strong>
                      </div>
                    </div>

                    {/* Expand toggle */}
                    {explanation && (
                      <button
                        type="button"
                        onClick={() => setExpandedSpec(isExpanded ? null : r.specialization_name)}
                        aria-expanded={isExpanded}
                        style={{
                          width: '28px', height: '28px', borderRadius: '6px',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          background: 'var(--color-surface-elevated)', border: '1px solid var(--color-border)',
                          color: 'var(--color-text-muted)', cursor: 'pointer', flexShrink: 0,
                          transition: 'all 120ms ease',
                        }}
                        className="focus-ring"
                        onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--color-text-primary)'; e.currentTarget.style.background = 'var(--color-surface-hover)'; }}
                        onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--color-text-muted)'; e.currentTarget.style.background = 'var(--color-surface-elevated)'; }}
                      >
                        {isExpanded ? <ChevronUp style={{ width: '14px', height: '14px' }} /> : <ChevronDown style={{ width: '14px', height: '14px' }} />}
                      </button>
                    )}
                  </div>

                  {/* XAI drawer */}
                  {isExpanded && explanation && (
                    <div style={{ borderTop: '1px solid var(--color-border-subtle)', padding: '14px 16px', background: 'var(--color-bg-secondary)' }} className="animate-fadeIn">
                      {/* Summary */}
                      <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: '0 0 12px', lineHeight: 1.6 }}>
                        {explanation.summary}
                      </p>

                      {/* Strengths / weaknesses */}
                      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '12px' }}>
                        <div style={{ padding: '10px 12px', background: 'var(--color-success-subtle)', border: '1px solid var(--color-success-border)', borderRadius: '8px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                            <Check style={{ width: '12px', height: '12px', color: 'var(--color-success)' }} />
                            <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-success)' }}>Strengths</span>
                          </div>
                          <ul style={{ margin: 0, padding: '0 0 0 14px', fontSize: '11px', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>
                            {explanation.strengths.map((s, i) => <li key={i}>{s}</li>)}
                          </ul>
                        </div>
                        <div style={{ padding: '10px 12px', background: 'var(--color-warning-subtle)', border: '1px solid var(--color-warning-border)', borderRadius: '8px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                            <AlertCircle style={{ width: '12px', height: '12px', color: 'var(--color-warning)' }} />
                            <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-warning)' }}>Growth areas</span>
                          </div>
                          <ul style={{ margin: 0, padding: '0 0 0 14px', fontSize: '11px', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>
                            {explanation.weaknesses.map((w, i) => <li key={i}>{w}</li>)}
                          </ul>
                        </div>
                      </div>

                      {/* Counterfactuals */}
                      {explanation.counterfactuals?.length > 0 && (
                        <div style={{ padding: '10px 12px', background: 'var(--color-primary-subtle)', border: '1px solid var(--color-primary-border)', borderRadius: '8px' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                            <TrendingUp style={{ width: '12px', height: '12px', color: 'var(--color-primary)' }} />
                            <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-primary)' }}>How to improve your standing</span>
                          </div>
                          {explanation.counterfactuals.map((cf, i) => (
                            <p key={i} style={{ margin: '2px 0 0', fontSize: '11px', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>{cf}</p>
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

        {/* Right: ML panel */}
        <div>
          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.04em', marginBottom: '10px', textTransform: 'uppercase' }}>
            ML cross-check
          </div>
          <div style={{
            background: 'var(--color-teal-subtle)', border: '1px solid var(--color-teal-border)',
            borderRadius: '10px', overflow: 'hidden',
          }}>
            {/* Panel header */}
            <div style={{ padding: '12px 14px', borderBottom: '1px solid var(--color-teal-border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Brain style={{ width: '13px', height: '13px', color: 'var(--color-teal)' }} />
                <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-teal)' }}>Random Forest</span>
              </div>
              <Badge variant="teal" size="sm">ML</Badge>
            </div>

            <div style={{ padding: '14px' }}>
              <p style={{ fontSize: '11px', color: 'var(--color-text-secondary)', margin: '0 0 12px', lineHeight: 1.5 }}>
                Supervised ML independently evaluates transcript patterns, separate from the rule engine.
              </p>

              {ml ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {/* Prediction */}
                  <div style={{
                    padding: '10px 12px', background: 'rgba(20,184,166,0.08)',
                    border: '1px solid var(--color-teal-border)', borderRadius: '8px',
                    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  }}>
                    <div>
                      <div style={{ fontSize: '10px', color: 'var(--color-text-muted)', fontWeight: 600, letterSpacing: '0.04em', marginBottom: '3px' }}>ML PREDICTION</div>
                      <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--color-text-primary)' }}>{ml.prediction}</div>
                    </div>
                    <Badge variant={ml.consensus ? 'success' : 'teal'} size="sm">{ml.confidence_label}</Badge>
                  </div>

                  {/* Probabilities */}
                  {ml.probabilities && (
                    <div>
                      <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '8px' }}>Class probabilities</div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '7px' }}>
                        {Object.entries(ml.probabilities).map(([label, prob]) => {
                          const pct = Math.round(prob * 100);
                          return (
                            <div key={label}>
                              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--color-text-secondary)', marginBottom: '3px' }}>
                                <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', paddingRight: '8px' }}>{label}</span>
                                <span style={{ fontWeight: 600, color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums', flexShrink: 0 }}>{pct}%</span>
                              </div>
                              <div style={{ height: '3px', background: 'rgba(255,255,255,0.1)', borderRadius: '2px', overflow: 'hidden' }}>
                                <div style={{ width: `${pct}%`, height: '100%', background: 'var(--color-teal)', borderRadius: '2px', transition: 'width 600ms cubic-bezier(0.25,1,0.5,1)' }} />
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Preliminary warning */}
                  {ml.is_preliminary && (
                    <div style={{ display: 'flex', gap: '6px', padding: '8px 10px', background: 'var(--color-warning-subtle)', border: '1px solid var(--color-warning-border)', borderRadius: '8px', fontSize: '11px', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
                      <Info style={{ width: '12px', height: '12px', color: 'var(--color-warning)', flexShrink: 0, marginTop: '1px' }} />
                      <span>Fewer than 3 core areas evaluated. Confidence increases with more completed courses.</span>
                    </div>
                  )}
                </div>
              ) : (
                <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', margin: 0 }}>
                  ML inference pending or unavailable.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* ── Navigation ───────────────────────────────────────────── */}
      <div style={{ paddingTop: '20px', borderTop: '1px solid var(--color-border-subtle)', display: 'flex', justifyContent: 'space-between', marginTop: '24px' }}>
        <Button variant="secondary" size="md" icon={ArrowLeft} onClick={onPrev}>Interests</Button>
        <Button variant="primary" size="lg" icon={ArrowRight} iconPosition="right" onClick={onNext}>Elective advisor</Button>
      </div>

      <style>{`
        @media (max-width: 768px) {
          .recs-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  );
}
