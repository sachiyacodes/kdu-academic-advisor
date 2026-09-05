import React, { useState } from 'react';
import {
  Check, AlertCircle, Clock, Unlock, ArrowRight, ArrowLeft,
} from 'lucide-react';
import { Button, Badge, Skeleton } from './ui';

function TabBar({ tabs, active, onChange }) {
  return (
    <div style={{
      display: 'flex', gap: '2px', background: 'var(--color-bg-secondary)',
      border: '1px solid var(--color-border)', borderRadius: '10px', padding: '3px',
      overflowX: 'auto',
    }}>
      {tabs.map((t) => {
        const isActive = active === t.id;
        return (
          <button
            key={t.id}
            type="button"
            onClick={() => onChange(t.id)}
            style={{
              display: 'flex', alignItems: 'center', gap: '6px',
              padding: '6px 14px', borderRadius: '8px', border: 'none', cursor: 'pointer',
              fontSize: '12px', fontWeight: isActive ? 600 : 400, whiteSpace: 'nowrap',
              transition: 'all 120ms ease', flexShrink: 0,
              background: isActive ? 'var(--color-surface)' : 'transparent',
              color: isActive ? 'var(--color-text-primary)' : 'var(--color-text-muted)',
              boxShadow: isActive ? '0 1px 3px rgba(0,0,0,0.15)' : 'none',
            }}
            className="focus-ring"
          >
            {t.label}
            {t.count != null && (
              <span style={{
                fontSize: '10px', fontWeight: 600, padding: '1px 6px', borderRadius: '10px',
                background: isActive ? 'var(--color-primary-subtle)' : 'var(--color-surface-elevated)',
                color: isActive ? 'var(--color-primary)' : 'var(--color-text-muted)',
                border: '1px solid', borderColor: isActive ? 'var(--color-primary-border)' : 'var(--color-border)',
              }}>
                {t.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}

function ElectiveCard({ item, isNow }) {
  return (
    <div style={{
      background: 'var(--color-surface)', borderRadius: '10px', overflow: 'hidden',
      border: '1px solid var(--color-border)',
      borderLeft: `3px solid ${isNow ? 'var(--color-success)' : 'var(--color-border)'}`,
    }}>
      <div style={{ padding: '12px 14px' }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '10px', marginBottom: '8px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <span className="course-code" style={{ color: isNow ? 'var(--color-success)' : 'var(--color-text-secondary)' }}>
                {item.course.course_code}
              </span>
              <span style={{
                fontSize: '10px', padding: '1px 7px', borderRadius: '4px',
                background: 'var(--color-surface-elevated)', border: '1px solid var(--color-border)',
                color: 'var(--color-text-muted)',
              }}>
                {item.course.credits} cr · Y{item.course.year}S{item.course.semester}
              </span>
            </div>
            <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)', lineHeight: 1.3 }}>
              {item.course.course_name}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '2px' }}>
              {item.course.subject_area}
            </div>
          </div>

          {/* Synergy score */}
          <div style={{ textAlign: 'right', flexShrink: 0 }}>
            <div style={{ fontSize: '10px', color: 'var(--color-text-muted)', fontWeight: 600, letterSpacing: '0.04em', marginBottom: '2px' }}>SYNERGY</div>
            <div style={{
              fontSize: '16px', fontWeight: 800, fontVariantNumeric: 'tabular-nums',
              color: isNow ? 'var(--color-primary)' : 'var(--color-text-secondary)',
            }}>
              {item.synergy_score}%
            </div>
          </div>
        </div>

        <p style={{
          fontSize: '11px', color: 'var(--color-text-secondary)', lineHeight: 1.5, margin: 0,
          padding: '8px 10px', background: 'var(--color-bg-secondary)',
          border: '1px solid var(--color-border-subtle)', borderRadius: '6px',
        }}>
          {item.reason}
        </p>

        {item.chain_impact_count > 0 && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '8px', fontSize: '11px', color: 'var(--color-warning)', fontWeight: 500 }}>
            <Unlock style={{ width: '12px', height: '12px', flexShrink: 0 }} />
            Unlocks {item.chain_impact_count} advanced course{item.chain_impact_count > 1 ? 's' : ''}
          </div>
        )}
      </div>
    </div>
  );
}

export default function StepElectives({
  advisorData, loading, targetSpec, setTargetSpec, specializations, onPrev, onNext,
}) {
  const [activeTab, setActiveTab] = useState('electives');

  if (loading) {
    return (
      <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>
        <div style={{ padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)', marginBottom: '24px' }}>
          <Skeleton className="h-7 w-72" />
          <Skeleton className="h-4 w-96 mt-2" />
        </div>
        <Skeleton className="h-12 w-full mb-6" />
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
          {[1,2,3,4].map(i => <Skeleton key={i} className="h-32 w-full" />)}
        </div>
      </div>
    );
  }

  if (!advisorData) {
    return (
      <div style={{ maxWidth: '480px', margin: '64px auto', textAlign: 'center' }}>
        <AlertCircle style={{ width: '32px', height: '32px', color: 'var(--color-warning)', margin: '0 auto 16px' }} />
        <h2 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--color-text-primary)', margin: '0 0 8px' }}>No advisor data</h2>
        <Button variant="primary" size="md" onClick={onPrev}>Back to recommendations</Button>
      </div>
    );
  }

  const { electives = [], core_courses = [], roadmap = {} } = advisorData;
  const recNow   = electives.filter((e) => e.category === 'Recommended Now');
  const recLater = electives.filter((e) => e.category === 'Recommended Later');

  const tabs = [
    { id: 'electives', label: 'Personalized electives', count: electives.length },
    { id: 'cores',     label: 'Core pathways',          count: core_courses.length },
    { id: 'roadmap',   label: '4-Year roadmap' },
  ];

  return (
    <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>

      {/* ── Header ───────────────────────────────────────────────── */}
      <div style={{
        padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '24px',
      }}>
        <div>
          <h1 style={{ fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em', color: 'var(--color-text-primary)', margin: 0, lineHeight: 1.3 }}>
            Elective Advisor
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: '6px 0 0', lineHeight: 1.6 }}>
            Prerequisite validation, stage eligibility, and specialization synergy scoring.
          </p>
        </div>

        {/* Target spec selector */}
        <div style={{ flexShrink: 0 }}>
          <label htmlFor="target-spec-select" style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '6px', letterSpacing: '0.03em' }}>
            Target pathway
          </label>
          <select
            id="target-spec-select"
            value={targetSpec}
            onChange={(e) => setTargetSpec(e.target.value)}
            style={{
              background: 'var(--color-surface)', border: '1px solid var(--color-border)',
              borderRadius: '8px', padding: '6px 12px', fontSize: '12px', fontWeight: 600,
              color: 'var(--color-primary)', cursor: 'pointer', outline: 'none',
            }}
            className="focus-ring"
          >
            {specializations?.map((s) => (
              <option key={s.specialization_id} value={s.name} style={{ background: 'var(--color-surface)', color: 'var(--color-text-primary)', fontWeight: 400 }}>
                {s.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* ── Tabs ─────────────────────────────────────────────────── */}
      <div style={{ margin: '20px 0' }}>
        <TabBar tabs={tabs} active={activeTab} onChange={setActiveTab} />
      </div>

      {/* ── Tab: Electives ───────────────────────────────────────── */}
      {activeTab === 'electives' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>

          {/* Now */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
              <Check style={{ width: '13px', height: '13px', color: 'var(--color-success)' }} />
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-success)' }}>
                Available now
              </span>
              <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>— prerequisites met & stage eligible</span>
              <span style={{
                fontSize: '10px', padding: '1px 7px', borderRadius: '10px', marginLeft: '4px',
                background: 'var(--color-success-subtle)', border: '1px solid var(--color-success-border)',
                color: 'var(--color-success)', fontWeight: 600,
              }}>{recNow.length}</span>
            </div>

            {recNow.length === 0 ? (
              <div style={{ padding: '32px', textAlign: 'center', border: '1px dashed var(--color-border)', borderRadius: '10px', fontSize: '12px', color: 'var(--color-text-muted)' }}>
                No electives currently eligible. Check prerequisites in the later list.
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }} className="elec-grid">
                {recNow.map((item) => <ElectiveCard key={item.course.course_code} item={item} isNow={true} />)}
              </div>
            )}
          </div>

          {/* Later */}
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
              <Clock style={{ width: '13px', height: '13px', color: 'var(--color-warning)' }} />
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-warning)' }}>
                Recommended later
              </span>
              <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>— pending prerequisites or future stage</span>
              <span style={{
                fontSize: '10px', padding: '1px 7px', borderRadius: '10px', marginLeft: '4px',
                background: 'var(--color-warning-subtle)', border: '1px solid var(--color-warning-border)',
                color: 'var(--color-warning)', fontWeight: 600,
              }}>{recLater.length}</span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }} className="elec-grid">
              {recLater.slice(0, 10).map((item) => <ElectiveCard key={item.course.course_code} item={item} isNow={false} />)}
            </div>
          </div>
        </div>
      )}

      {/* ── Tab: Core courses ────────────────────────────────────── */}
      {activeTab === 'cores' && (
        <div style={{
          border: '1px solid var(--color-border)', borderRadius: '10px', overflow: 'hidden',
        }}>
          <table className="academic-table">
            <thead>
              <tr>
                <th>Code</th>
                <th>Course</th>
                <th>Subject area</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {core_courses.map((item) => (
                <tr key={item.course.course_code}>
                  <td><span className="course-code">{item.course.course_code}</span></td>
                  <td>
                    <div style={{ fontWeight: 500, fontSize: '12px' }}>{item.course.course_name}</div>
                    <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '1px' }}>{item.course.credits} cr · Y{item.course.year}S{item.course.semester}</div>
                  </td>
                  <td style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>{item.course.subject_area}</td>
                  <td>
                    <Badge variant={item.category === 'Recommended Now' ? 'success' : 'neutral'} size="sm">
                      {item.category}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* ── Tab: Roadmap ─────────────────────────────────────────── */}
      {activeTab === 'roadmap' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {Object.entries(roadmap).map(([year, sems]) => (
            <div key={year} style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: '10px', overflow: 'hidden' }}>
              <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--color-border-subtle)', background: 'var(--color-bg-secondary)' }}>
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--color-text-primary)' }}>{year}</span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0' }} className="roadmap-grid">
                {Object.entries(sems).map(([sem, coursesList], si) => (
                  <div key={sem} style={{ padding: '14px 16px', borderRight: si === 0 ? '1px solid var(--color-border-subtle)' : 'none' }}>
                    <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-primary)', marginBottom: '10px' }}>
                      {sem} · {coursesList.length} courses
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      {coursesList.map((c) => (
                        <div key={c.course_code} style={{
                          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                          padding: '6px 10px', background: 'var(--color-bg-secondary)',
                          border: '1px solid var(--color-border-subtle)', borderRadius: '6px', fontSize: '11px',
                        }}>
                          <div>
                            <span className="course-code" style={{ fontSize: '11px' }}>{c.course_code}</span>
                            <span style={{ color: 'var(--color-text-secondary)', marginLeft: '8px' }}>{c.course_name}</span>
                          </div>
                          <span style={{ color: 'var(--color-text-muted)', flexShrink: 0, marginLeft: '8px' }}>{c.credits} cr</span>
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

      {/* ── Navigation ───────────────────────────────────────────── */}
      <div style={{ paddingTop: '20px', borderTop: '1px solid var(--color-border-subtle)', display: 'flex', justifyContent: 'space-between', marginTop: '24px' }}>
        <Button variant="secondary" size="md" icon={ArrowLeft} onClick={onPrev}>Recommendations</Button>
        <Button variant="primary" size="lg" icon={ArrowRight} iconPosition="right" onClick={onNext}>Graduation audit</Button>
      </div>

      <style>{`
        @media (max-width: 640px) {
          .elec-grid  { grid-template-columns: 1fr !important; }
          .roadmap-grid { grid-template-columns: 1fr !important; }
          .roadmap-grid > div { border-right: none !important; border-bottom: 1px solid var(--color-border-subtle); }
        }
      `}</style>
    </div>
  );
}
