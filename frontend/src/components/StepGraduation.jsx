import React from 'react';
import {
  GraduationCap, Check, AlertTriangle, BarChart3,
  ArrowLeft, RotateCcw, BookOpen, Info,
} from 'lucide-react';
import { Button, Skeleton } from './ui';

function StatBox({ label, value, sub, color }) {
  return (
    <div style={{
      background: 'var(--color-surface)', border: '1px solid var(--color-border)',
      borderRadius: '10px', padding: '14px 16px',
    }}>
      <div style={{ fontSize: '10px', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.05em', marginBottom: '6px' }}>
        {label}
      </div>
      <div style={{ fontSize: '20px', fontWeight: 800, letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums', color: color || 'var(--color-text-primary)', lineHeight: 1.1 }}>
        {value}
      </div>
      {sub && (
        <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '4px' }}>{sub}</div>
      )}
    </div>
  );
}

function CreditProgress({ label, sub, earned, target, pct, color }) {
  return (
    <div style={{
      background: 'var(--color-surface)', border: '1px solid var(--color-border)',
      borderRadius: '10px', padding: '16px 18px',
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

      <div style={{ height: '4px', background: 'var(--color-border)', borderRadius: '2px', overflow: 'hidden', marginBottom: '8px' }}>
        <div style={{
          width: `${Math.min(100, pct)}%`, height: '100%', borderRadius: '2px',
          background: color || 'var(--color-primary)',
          transition: 'width 700ms cubic-bezier(0.25, 1, 0.5, 1)',
        }} />
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px' }}>
        <span style={{ fontWeight: 600, color: color || 'var(--color-primary)' }}>{pct}% complete</span>
        <span style={{ color: 'var(--color-text-muted)' }}>
          {Math.max(0, target - earned)} credits remaining
        </span>
      </div>
    </div>
  );
}

export default function StepGraduation({ auditData, recData, loading, onPrev, onReset }) {

  if (loading) {
    return (
      <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>
        <div style={{ padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)', marginBottom: '24px' }}>
          <Skeleton className="h-7 w-72" />
          <Skeleton className="h-4 w-96 mt-2" />
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', marginBottom: '20px' }}>
          {[1,2,3,4].map(i => <Skeleton key={i} className="h-20 w-full" />)}
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
          <Skeleton className="h-32 w-full" />
          <Skeleton className="h-32 w-full" />
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

  const profile = recData?.profile;
  const subjectPerfs = profile?.subject_performances || [];

  return (
    <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>

      {/* ── Header ───────────────────────────────────────────────── */}
      <div style={{
        padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '24px',
      }}>
        <div>
          <h1 style={{ fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em', color: 'var(--color-text-primary)', margin: 0, lineHeight: 1.3 }}>
            Graduation Audit
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: '6px 0 0', lineHeight: 1.6 }}>
            Verification against official requirements: 120 GPA credits + 14 NGPA credits.
          </p>
        </div>

        {/* Clearance status */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '10px', flexShrink: 0,
          padding: '10px 14px', borderRadius: '10px',
          background: is_eligible ? 'var(--color-success-subtle)' : 'var(--color-surface)',
          border: `1px solid ${is_eligible ? 'var(--color-success-border)' : 'var(--color-border)'}`,
        }}>
          <div style={{
            width: '32px', height: '32px', borderRadius: '50%', flexShrink: 0,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: is_eligible ? 'var(--color-success)' : 'var(--color-primary-subtle)',
            color: is_eligible ? '#fff' : 'var(--color-primary)',
            border: is_eligible ? 'none' : '1px solid var(--color-primary-border)',
          }}>
            <GraduationCap style={{ width: '16px', height: '16px' }} />
          </div>
          <div>
            <div style={{ fontSize: '10px', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.04em', marginBottom: '2px' }}>CLEARANCE</div>
            <div style={{ fontSize: '12px', fontWeight: 700, color: is_eligible ? 'var(--color-success)' : 'var(--color-text-primary)' }}>
              {is_eligible ? 'Requirements met' : 'Degree in progress'}
            </div>
          </div>
        </div>
      </div>

      {/* ── Stats row ────────────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px', margin: '20px 0' }} className="stats-grid">
        <StatBox
          label="ACADEMIC STAGE"
          value={profile ? `Y${profile.year}S${profile.semester}` : '—'}
          sub={profile ? `Year ${profile.year}, Semester ${profile.semester}` : 'Enrolled'}
        />
        <StatBox
          label="CUMULATIVE GPA"
          value={gpa ? gpa.toFixed(2) : '0.00'}
          color="var(--color-primary)"
        />
        <StatBox
          label="CLASSIFICATION"
          value={classification || 'Good Standing'}
          color="var(--color-success)"
          sub={classification ? '' : undefined}
        />
        <StatBox
          label="TOTAL CREDITS"
          value={`${total_credits_earned || gpa_credits_earned + ngpa_credits_earned}`}
          sub="of 134 required"
        />
      </div>

      {/* ── Credit progress ──────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }} className="progress-grid">
        <CreditProgress
          label="Core & Elective Credits"
          sub={`Core ${core_credits} cr · Elective ${elective_credits} cr`}
          earned={gpa_credits_earned}
          target={gpa_target}
          pct={gpa_progress_pct}
          color="var(--color-primary)"
        />
        <CreditProgress
          label="Non-GPA Credits"
          sub="English, Internship, Leadership"
          earned={ngpa_credits_earned}
          target={ngpa_target}
          pct={ngpa_progress_pct}
          color="var(--color-teal)"
        />
      </div>

      {/* ── Bottlenecks ──────────────────────────────────────────── */}
      {bottlenecks.length > 0 ? (
        <div style={{
          padding: '14px 16px', marginBottom: '20px',
          background: 'var(--color-warning-subtle)', border: '1px solid var(--color-warning-border)',
          borderRadius: '10px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '8px' }}>
            <AlertTriangle style={{ width: '14px', height: '14px', color: 'var(--color-warning)', flexShrink: 0 }} />
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-warning)' }}>
              Prerequisite bottlenecks
            </span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--color-text-secondary)', margin: '0 0 8px', lineHeight: 1.5 }}>
            These courses unlock multiple downstream subjects. Complete them to avoid progression delays.
          </p>
          <ul style={{ margin: 0, padding: '0 0 0 16px', fontSize: '12px', color: 'var(--color-text-primary)', lineHeight: 1.8 }}>
            {bottlenecks.map((b, i) => <li key={i}>{b}</li>)}
          </ul>
        </div>
      ) : (
        <div style={{
          display: 'flex', alignItems: 'center', gap: '10px',
          padding: '12px 16px', marginBottom: '20px',
          background: 'var(--color-success-subtle)', border: '1px solid var(--color-success-border)',
          borderRadius: '10px',
        }}>
          <div style={{
            width: '28px', height: '28px', borderRadius: '50%', flexShrink: 0,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            background: 'rgba(34,197,94,0.2)', color: 'var(--color-success)',
          }}>
            <Check style={{ width: '14px', height: '14px' }} />
          </div>
          <div>
            <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>No prerequisite bottlenecks</div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)' }}>All prerequisite chains for your current stage are satisfied.</div>
          </div>
        </div>
      )}

      {/* ── Policy notes ─────────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '20px' }} className="notes-grid">
        <div style={{
          padding: '12px 14px', background: 'var(--color-surface)',
          border: '1px solid var(--color-border)', borderRadius: '10px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
            <BookOpen style={{ width: '12px', height: '12px', color: 'var(--color-primary)' }} />
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>Electives policy</span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--color-text-secondary)', margin: 0, lineHeight: 1.6 }}>
            KDU computing electives begin in <strong style={{ color: 'var(--color-text-primary)' }}>Year 3, Semester 2</strong>. Years 1 & 2 are mandatory core foundations.
          </p>
        </div>
        <div style={{
          padding: '12px 14px', background: 'var(--color-surface)',
          border: '1px solid var(--color-border)', borderRadius: '10px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
            <Info style={{ width: '12px', height: '12px', color: 'var(--color-teal)' }} />
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>Stage-aware audit</span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--color-text-secondary)', margin: 0, lineHeight: 1.6 }}>
            Evaluation includes {gpa_credits_earned} GPA + {ngpa_credits_earned} NGPA credits from completed semesters. Adjust grades in Step 2.
          </p>
        </div>
      </div>

      {/* ── Subject performance ──────────────────────────────────── */}
      {subjectPerfs.length > 0 && (
        <div style={{
          background: 'var(--color-surface)', border: '1px solid var(--color-border)',
          borderRadius: '10px', padding: '18px', marginBottom: '20px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', paddingBottom: '12px', borderBottom: '1px solid var(--color-border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
              <BarChart3 style={{ width: '14px', height: '14px', color: 'var(--color-primary)' }} />
              <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-text-primary)' }}>Performance by subject area</span>
            </div>
            <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
              {subjectPerfs.length} areas
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px 32px' }} className="perf-grid">
            {subjectPerfs.map((p) => {
              const mark = p.average_mark;
              const barColor = mark >= 80 ? 'var(--color-success)' : mark < 55 ? 'var(--color-warning)' : 'var(--color-primary)';
              const textColor = mark >= 80 ? 'var(--color-success)' : mark < 55 ? 'var(--color-warning)' : 'var(--color-primary)';
              const courses = p.course_count === 1 ? '1 course' : `${p.course_count} courses`;

              return (
                <div key={p.subject_area}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '5px' }}>
                    <span style={{ fontSize: '12px', color: 'var(--color-text-primary)', fontWeight: 500 }}>{p.subject_area}</span>
                    <span style={{ fontSize: '11px', fontWeight: 700, color: textColor, fontVariantNumeric: 'tabular-nums', flexShrink: 0, marginLeft: '8px' }}>
                      {mark.toFixed(1)}%
                      <span style={{ fontSize: '10px', fontWeight: 400, color: 'var(--color-text-muted)', marginLeft: '4px' }}>({courses})</span>
                    </span>
                  </div>
                  <div style={{ height: '3px', background: 'var(--color-border)', borderRadius: '2px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${Math.min(100, mark)}%`, height: '100%', borderRadius: '2px',
                      background: barColor, transition: 'width 600ms cubic-bezier(0.25,1,0.5,1)',
                    }} />
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
          .stats-grid    { grid-template-columns: 1fr 1fr !important; }
          .progress-grid { grid-template-columns: 1fr !important; }
          .notes-grid    { grid-template-columns: 1fr !important; }
          .perf-grid     { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  );
}
