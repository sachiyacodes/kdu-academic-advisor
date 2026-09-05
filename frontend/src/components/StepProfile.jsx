import React from 'react';
import { BookOpen, Calendar, ArrowRight, School, Sparkles, Info } from 'lucide-react';
import { Button, Badge } from './ui';

export default function StepProfile({
  profile,
  setProfile,
  degrees,
  demoProfiles,
  onLoadDemo,
  onNext,
}) {
  return (
    <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>

      {/* ── Page header ──────────────────────────────────────────── */}
      <div style={{ padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)' }}>
        <h1 style={{
          fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em',
          color: 'var(--color-text-primary)', margin: 0, lineHeight: 1.3,
        }}>
          Academic Profile
        </h1>
        <p style={{
          fontSize: '13px', color: 'var(--color-text-secondary)', margin: '6px 0 0',
          maxWidth: '520px', lineHeight: 1.6,
        }}>
          Set your enrolled degree and current academic stage. The advisor will use this to determine
          which courses you have completed and what requirements remain.
        </p>
      </div>

      {/* ── Two-column layout ────────────────────────────────────── */}
      <div style={{
        display: 'grid', gridTemplateColumns: '1fr 320px', gap: '32px',
        paddingTop: '28px', alignItems: 'start',
      }} className="profile-grid">

        {/* Left: form */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

          {/* Degree select */}
          <div>
            <label
              htmlFor="degree-select"
              style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}
            >
              <School style={{ width: '13px', height: '13px', color: 'var(--color-text-muted)' }} />
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-secondary)' }}>
                Enrolled degree program
              </span>
            </label>
            <select
              id="degree-select"
              value={profile.degree}
              onChange={(e) => setProfile({ ...profile, degree: e.target.value })}
              style={{
                width: '100%', height: '40px',
                background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)',
                borderRadius: '8px', padding: '0 12px', fontSize: '13px',
                color: 'var(--color-text-primary)', cursor: 'pointer',
                outline: 'none', transition: 'border-color 120ms ease',
              }}
              className="focus-ring"
            >
              {degrees.map((d) => {
                const name = d.name || d.degree_name;
                return (
                  <option key={d.degree_id} value={name} style={{ background: 'var(--color-surface)' }}>
                    {name}
                  </option>
                );
              })}
            </select>

            {profile.degree === 'Custom / Other University Degree' && (
              <div style={{
                display: 'flex', gap: '8px', padding: '10px 12px', marginTop: '8px',
                background: 'var(--color-info-subtle)', border: '1px solid rgba(56,189,248,0.2)',
                borderRadius: '8px', fontSize: '12px',
              }}>
                <Info style={{ width: '13px', height: '13px', color: 'var(--color-info)', flexShrink: 0, marginTop: '1px' }} />
                <span style={{ color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
                  Universal mode — enables manual course entry and access to all 89 electives.
                </span>
              </div>
            )}
          </div>

          {/* Year + Semester row */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>

            {/* Academic year */}
            <div>
              <label style={{
                display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px',
              }}>
                <Calendar style={{ width: '13px', height: '13px', color: 'var(--color-text-muted)' }} />
                <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-secondary)' }}>
                  Current academic year
                </span>
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px' }}>
                {[1, 2, 3, 4].map((y) => {
                  const sel = profile.year === y;
                  return (
                    <button
                      key={y}
                      type="button"
                      onClick={() => setProfile({ ...profile, year: y })}
                      aria-pressed={sel}
                      style={{
                        height: '36px', borderRadius: '8px', border: '1px solid',
                        fontSize: '12px', fontWeight: sel ? 600 : 400, cursor: 'pointer',
                        transition: 'all 120ms ease',
                        background: sel ? 'var(--color-primary)' : 'var(--color-bg-secondary)',
                        borderColor: sel ? 'transparent' : 'var(--color-border)',
                        color: sel ? '#fff' : 'var(--color-text-secondary)',
                      }}
                      className="focus-ring"
                    >
                      Y{y}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Semester */}
            <div>
              <label style={{
                display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px',
              }}>
                <BookOpen style={{ width: '13px', height: '13px', color: 'var(--color-text-muted)' }} />
                <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-secondary)' }}>
                  Current semester
                </span>
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px' }}>
                {[1, 2].map((s) => {
                  const sel = profile.semester === s;
                  return (
                    <button
                      key={s}
                      type="button"
                      onClick={() => setProfile({ ...profile, semester: s })}
                      aria-pressed={sel}
                      style={{
                        height: '36px', borderRadius: '8px', border: '1px solid',
                        fontSize: '12px', fontWeight: sel ? 600 : 400, cursor: 'pointer',
                        transition: 'all 120ms ease',
                        background: sel ? 'var(--color-primary)' : 'var(--color-bg-secondary)',
                        borderColor: sel ? 'transparent' : 'var(--color-border)',
                        color: sel ? '#fff' : 'var(--color-text-secondary)',
                      }}
                      className="focus-ring"
                    >
                      Sem {s}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Stage summary */}
          <div style={{
            padding: '12px 14px',
            background: 'var(--color-surface)', border: '1px solid var(--color-border-subtle)',
            borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '10px',
          }}>
            <div style={{
              width: '6px', height: '6px', borderRadius: '50%',
              background: 'var(--color-primary)', flexShrink: 0,
            }} />
            <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>
              Currently at{' '}
              <strong style={{ color: 'var(--color-text-primary)' }}>
                Year {profile.year}, Semester {profile.semester}
              </strong>
              . All prior semesters will be treated as completed.
            </span>
          </div>

          {/* Action */}
          <div style={{ paddingTop: '8px', borderTop: '1px solid var(--color-border-subtle)', textAlign: 'right' }}>
            <Button variant="primary" size="lg" onClick={onNext} icon={ArrowRight} iconPosition="right">
              Continue to Course History
            </Button>
          </div>
        </div>

        {/* Right: archetypes */}
        <div style={{
          background: 'var(--color-surface)', border: '1px solid var(--color-border)',
          borderRadius: '12px', overflow: 'hidden',
        }}>
          {/* Header */}
          <div style={{
            padding: '14px 16px', borderBottom: '1px solid var(--color-border-subtle)',
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
              <Sparkles style={{ width: '13px', height: '13px', color: 'var(--color-teal)' }} />
              <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>
                Student archetypes
              </span>
            </div>
            <Badge variant="teal" size="sm">
              Y{profile.year}S{profile.semester}
            </Badge>
          </div>

          {/* Description */}
          <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--color-border-subtle)' }}>
            <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', margin: 0, lineHeight: 1.5 }}>
              Pre-configured mark sets adapted to your current stage. Loads courses completed before
              Year {profile.year}, Sem {profile.semester}.
            </p>
          </div>

          {/* Archetype list */}
          <div style={{ padding: '8px' }}>
            {demoProfiles && Object.entries(demoProfiles).map(([key, demo]) => (
              <button
                key={key}
                type="button"
                onClick={() => onLoadDemo(key)}
                style={{
                  width: '100%', textAlign: 'left', padding: '10px 12px', borderRadius: '8px',
                  background: 'none', border: '1px solid transparent',
                  cursor: 'pointer', transition: 'all 120ms ease', marginBottom: '2px',
                  display: 'block',
                }}
                className="focus-ring archetype-btn"
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'var(--color-surface-hover)';
                  e.currentTarget.style.borderColor = 'var(--color-border)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'none';
                  e.currentTarget.style.borderColor = 'transparent';
                }}
              >
                <div style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  marginBottom: '3px',
                }}>
                  <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>
                    {demo.title.split('—')[0].trim()}
                  </span>
                  <span style={{
                    fontSize: '10px', color: 'var(--color-text-muted)',
                    background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)',
                    borderRadius: '4px', padding: '1px 6px', fontWeight: 500,
                  }}>
                    Load
                  </span>
                </div>
                <p style={{
                  fontSize: '11px', color: 'var(--color-text-muted)', margin: 0,
                  lineHeight: 1.4, overflow: 'hidden',
                  display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
                }}>
                  {demo.description}
                </p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Responsive grid collapse */}
      <style>{`
        .profile-grid { grid-template-columns: 1fr 300px; }
        @media (max-width: 768px) {
          .profile-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  );
}
