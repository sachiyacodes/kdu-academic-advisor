import React from 'react';
import {
  GraduationCap, Check, AlertTriangle, BarChart3,
  ArrowLeft, RotateCcw, BookOpen, Info,
} from 'lucide-react';
import { Button, Skeleton } from './ui';

function CreditProgress({ label, sub, earned, target, pct, color }) {
  return (
    <div style={{
      background: 'var(--color-surface)', border: '1px solid var(--color-border)',
      borderRadius: '8px', padding: '16px 18px',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
        <div>
          <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: '3px' }}>{label}</div>
          <div style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>{sub}</div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <span style={{ fontSize: '22px', fontWeight: 800, color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums', letterSpacing: '-0.02em' }}>{earned}</span>
          <span style={{ fontSize: '12px', color: 'var(--color-text-muted)', fontWeight: 400 }}> / {target} cr</span>
        </div>
      </div>
      <div style={{ height: '3px', background: 'var(--color-border)', borderRadius: '2px', overflow: 'hidden', marginBottom: '8px' }}>
        <div style={{
          width: `${Math.min(100, pct)}%`, height: '100%', borderRadius: '2px',
          background: color || 'var(--color-primary)',
          transition: 'width 700ms cubic-bezier(0.25, 1, 0.5, 1)',
        }} />
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px' }}>
        <span style={{ fontWeight: 600, color: color || 'var(--color-primary)' }}>{pct}% complete</span>
        <span style={{ color: 'var(--color-text-muted)' }}>{Math.max(0, target - earned)} credits remaining</span>
      </div>
    </div>
  );
}

export default function StepGraduation({ auditData, recData, loading, onPrev, onReset }) {

  if (loading) {
    return (
      <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>
        <div style={{ padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)', marginBottom: '20px' }}>
          <Skeleton style={{ height: '28px', width: '280px', marginBottom: '8px' }} />
          <Skeleton style={{ height: '16px', width: '380px' }} />
        </div>
        <Skeleton style={{ height: '64px', width: '100%', marginBottom: '16px' }} />
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }}>
          <Skeleton style={{ height: '100px' }} />
          <Skeleton style={{ height: '100px' }} />
        </div>
      </div>
    );
  }

  if (!auditData) {
    return (
      <div style={{ maxWidth: '480px', margin: '64px auto', textAlign: 'center' }}>
        <AlertTriangle style={{ width: '32px', height: '32px', color: 'var(--color-warning)', margin: '0 auto 16px' }} />
        <h2 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--color-text-primary)', margin: '0 0 8px' }}>No audit data</h2>
        <Button variant="primary" size="md" onClick={onPrev}>Back to electives</Button>
      </div>
    );
  }

  const {
    gpa = 0, classification, core_credits = 0, elective_credits = 0,
    gpa_credits_earned = 0, gpa_target = 120, gpa_progress_pct = 0,
    ngpa_credits_earned = 0, ngpa_target = 14, ngpa_progress_pct = 0,
    total_credits_earned = 0, is_eligible = false, bottlenecks = [],
  } = auditData;

  const profile      = recData?.profile;
  const subjectPerfs = profile?.subject_performances || [];
  const totalEarned  = total_credits_earned || gpa_credits_earned + ngpa_credits_earned;

  // Stats: rendered as a single bordered row, not four separate cards
  const stats = [
    { label: 'Academic stage',   value: profile ? `Y${profile.year}S${profile.semester}` : '—',   sub: profile ? `Year ${profile.year}, Semester ${profile.semester}` : 'Enrolled', color: null },
    { label: 'Cumulative GPA',   value: gpa ? gpa.toFixed(2) : '0.00',                             sub: null,                                                                        color: 'var(--color-primary)' },
    { label: 'Classification',   value: classification || 'Good Standing',                         sub: null,                                                                        color: 'var(--color-success)' },
    { label: 'Total credits',    value: `${totalEarned}`,                                           sub: `of 134 required`,                                                           color: null },
  ];

  return (
    <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>

      {/* ── Header ───────────────────────────────────────────────── */}
      <div style={{
        padding: '32px 0 20px',
        borderBottom: '1px solid var(--color-border-subtle)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '24px',
      }}>
        <div>
          <h1 style={{
            fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em',
            color: 'var(--color-text-primary)', margin: 0, lineHeight: 1.3,
          }}>
            Graduation Audit
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: '5px 0 0', lineHeight: 1.5 }}>
            Verification against official requirements: 120 GPA credits + 14 NGPA credits.
          </p>
        </div>

        {/* Clearance badge — inline with header, not floating */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0,
          padding: '8px 12px', borderRadius: '8px',
          background: is_eligible ? 'var(--color-success-subtle)' : 'var(--color-surface)',
          border: `1px solid ${is_eligible ? 'var(--color-success-border)' : 'var(--color-border)'}`,
        }}>
          <GraduationCap style={{
            width: '14px', height: '14px', flexShrink: 0,
            color: is_eligible ? 'var(--color-success)' : 'var(--color-text-muted)',
          }} />
          <div>
            <div style={{ fontSize: '10px', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.04em' }}>CLEARANCE</div>
            <div style={{ fontSize: '12px', fontWeight: 700, color: is_eligible ? 'var(--color-success)' : 'var(--color-text-primary)', marginTop: '1px' }}>
              {is_eligible ? 'Requirements met' : 'Degree in progress'}
            </div>
          </div>
        </div>
      </div>

      {/* ── Stats — single unified row, not four separate cards ───── */}
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
        border: '1px solid var(--color-border)', borderRadius: '8px',
        overflow: 'hidden', margin: '20px 0',
        background: 'var(--color-surface)',
      }} className="stats-row">
        {stats.map((s, i) => (
          <div key={s.label} style={{
            padding: '14px 16px',
            borderRight: i < stats.length - 1 ? '1px solid var(--color-border)' : 'none',
          }}>
            <div style={{
              fontSize: '10px', fontWeight: 600, color: 'var(--color-text-muted)',
              letterSpacing: '0.05em', marginBottom: '6px', textTransform: 'uppercase',
            }}>
              {s.label}
            </div>
            <div style={{
              fontSize: '20px', fontWeight: 800, letterSpacing: '-0.02em',
              fontVariantNumeric: 'tabular-nums', lineHeight: 1.1,
              color: s.color || 'var(--color-text-primary)',
            }}>
              {s.value}
            </div>
            {s.sub && (
              <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '4px' }}>{s.sub}</div>
            )}
          </div>
        ))}
      </div>

      {/* ── Credit progress bars ─────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }} className="progress-grid">
        <CreditProgress
          label="Core & Elective Credits"
          sub={`Core ${core_credits} cr · Elective ${elective_credits} cr`}
          earned={gpa_credits_earned} target={gpa_target} pct={gpa_progress_pct}
          color="var(--color-primary)"
        />
        <CreditProgress
          label="Non-GPA Credits"
          sub="English, Internship, Leadership"
          earned={ngpa_credits_earned} target={ngpa_target} pct={ngpa_progress_pct}
          color="var(--color-teal)"
        />
      </div>

      {/* ── Bottlenecks ──────────────────────────────────────────── */}
      {bottlenecks.length > 0 ? (
        <div style={{
          padding: '14px 16px', marginBottom: '16px',
          background: 'var(--color-surface)',
          border: '1px solid var(--color-warning-border)',
          borderLeft: '3px solid var(--color-warning)',
          borderRadius: '0 8px 8px 0',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '6px' }}>
            <AlertTriangle style={{ width: '13px', height: '13px', color: 'var(--color-warning)', flexShrink: 0 }} />
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-warning)' }}>
              Prerequisite bottlenecks
            </span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: '0 0 8px', lineHeight: 1.5 }}>
            These courses unlock multiple downstream subjects. Complete them to avoid progression delays.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {bottlenecks.map((b, i) => (
              <div key={i} style={{
                fontSize: '12px', color: 'var(--color-text-primary)',
                padding: '6px 10px', background: 'var(--color-bg-secondary)',
                border: '1px solid var(--color-border-subtle)', borderRadius: '6px',
                lineHeight: 1.5,
              }}>
                {b}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div style={{
          display: 'flex', alignItems: 'center', gap: '10px',
          padding: '11px 14px', marginBottom: '16px',
          background: 'var(--color-surface)',
          border: '1px solid var(--color-success-border)',
          borderLeft: '3px solid var(--color-success)',
          borderRadius: '0 8px 8px 0',
        }}>
          <Check style={{ width: '13px', height: '13px', color: 'var(--color-success)', flexShrink: 0 }} />
          <div>
            <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>No prerequisite bottlenecks</div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)' }}>All prerequisite chains for your current stage are satisfied.</div>
          </div>
        </div>
      )}

      {/* ── Policy notes ─────────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '16px' }} className="notes-grid">
        {[
          {
            icon: BookOpen, color: 'var(--color-primary)', label: 'Electives policy',
            text: <>KDU computing electives begin in <strong style={{ color: 'var(--color-text-primary)' }}>Year 3, Semester 2</strong>. Years 1 &amp; 2 are mandatory core foundations.</>,
          },
          {
            icon: Info, color: 'var(--color-teal)', label: 'Stage-aware audit',
            text: <>Evaluation includes {gpa_credits_earned} GPA + {ngpa_credits_earned} NGPA credits from completed semesters. Adjust grades in Step 2.</>,
          },
        ].map(({ icon: Icon, color, label, text }) => (
          <div key={label} style={{
            padding: '12px 14px', background: 'var(--color-surface)',
            border: '1px solid var(--color-border)', borderRadius: '8px',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '5px' }}>
              <Icon style={{ width: '12px', height: '12px', color }} />
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>{label}</span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--color-text-secondary)', margin: 0, lineHeight: 1.6 }}>{text}</p>
          </div>
        ))}
      </div>

      {/* ── Subject performance ──────────────────────────────────── */}
      {subjectPerfs.length > 0 && (
        <div style={{
          background: 'var(--color-surface)', border: '1px solid var(--color-border)',
          borderRadius: '8px', padding: '16px 18px', marginBottom: '16px',
        }}>
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            marginBottom: '14px', paddingBottom: '10px',
            borderBottom: '1px solid var(--color-border-subtle)',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
              <BarChart3 style={{ width: '13px', height: '13px', color: 'var(--color-primary)' }} />
              <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-text-primary)' }}>Performance by subject area</span>
            </div>
            <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>{subjectPerfs.length} areas</span>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px 32px' }} className="perf-grid">
            {subjectPerfs.map((p) => {
              const mark   = p.average_mark;
              const bar    = mark >= 80 ? 'var(--color-success)' : mark < 55 ? 'var(--color-warning)' : 'var(--color-primary)';
              const label  = mark >= 80 ? 'var(--color-success)' : mark < 55 ? 'var(--color-warning)' : 'var(--color-primary)';
              const count  = p.course_count === 1 ? '1 course' : `${p.course_count} courses`;
              return (
                <div key={p.subject_area}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '5px' }}>
                    <span style={{ fontSize: '12px', color: 'var(--color-text-primary)', fontWeight: 500 }}>{p.subject_area}</span>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: label, fontVariantNumeric: 'tabular-nums', flexShrink: 0, marginLeft: '8px' }}>
                      {mark.toFixed(1)}%
                      <span style={{ fontSize: '10px', fontWeight: 400, color: 'var(--color-text-muted)', marginLeft: '4px' }}>({count})</span>
                    </span>
                  </div>
                  <div style={{ height: '3px', background: 'var(--color-border)', borderRadius: '2px', overflow: 'hidden' }}>
                    <div style={{ width: `${Math.min(100, mark)}%`, height: '100%', background: bar, borderRadius: '2px', transition: 'width 600ms cubic-bezier(0.25,1,0.5,1)' }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ── Navigation ───────────────────────────────────────────── */}
      <div style={{ paddingTop: '20px', borderTop: '1px solid var(--color-border-subtle)', display: 'flex', justifyContent: 'space-between' }}>
        <Button variant="secondary" size="md" icon={ArrowLeft} onClick={onPrev}>Electives</Button>
        <Button variant="secondary" size="md" icon={RotateCcw} onClick={onReset}>Start new evaluation</Button>
      </div>

      <style>{`
        @media (max-width: 640px) {
          .stats-row    { grid-template-columns: 1fr 1fr !important; }
          .stats-row > div { border-right: none !important; border-bottom: 1px solid var(--color-border); }
          .progress-grid { grid-template-columns: 1fr !important; }
          .notes-grid    { grid-template-columns: 1fr !important; }
          .perf-grid     { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  );
}
