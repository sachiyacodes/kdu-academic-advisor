import React from 'react';
import { GraduationCap, RotateCcw, Check } from 'lucide-react';

const STEPS = [
  { id: 1, label: 'Profile',         short: 'Profile' },
  { id: 2, label: 'Courses',         short: 'Courses' },
  { id: 3, label: 'Interests',       short: 'Interests' },
  { id: 4, label: 'Recommendations', short: 'Recs' },
  { id: 5, label: 'Electives',       short: 'Electives' },
  { id: 6, label: 'Graduation',      short: 'Graduation' },
];

export default function Navbar({
  currentStep,
  setCurrentStep,
  completedSteps,
  demoProfiles,
  onLoadDemo,
  onReset,
  backendOnline,
}) {
  const currentStepObj = STEPS.find((s) => s.id === currentStep) || STEPS[0];

  return (
    <header
      style={{
        background: 'var(--color-bg-secondary)',
        borderBottom: '1px solid var(--color-border)',
        position: 'sticky',
        top: 0,
        zIndex: 50,
        backdropFilter: 'blur(12px)',
      }}
    >
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 24px' }}>

        {/* ── Top bar ───────────────────────────────────────────── */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '56px' }}>

          {/* Brand */}
          <button
            type="button"
            onClick={() => setCurrentStep(1)}
            aria-label="Go to Step 1: Student Profile"
            style={{
              display: 'flex', alignItems: 'center', gap: '10px',
              background: 'none', border: 'none', cursor: 'pointer', padding: '4px',
              borderRadius: '8px',
            }}
            className="focus-ring"
          >
            <div style={{
              width: '32px', height: '32px', borderRadius: '8px',
              background: 'var(--color-primary-subtle)',
              border: '1px solid var(--color-primary-border)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              color: 'var(--color-primary)', flexShrink: 0,
            }}>
              <GraduationCap style={{ width: '16px', height: '16px' }} />
            </div>
            <div style={{ textAlign: 'left' }}>
              <div style={{
                fontSize: '14px', fontWeight: 700, letterSpacing: '-0.01em',
                color: 'var(--color-text-primary)', lineHeight: 1.2,
              }}>
                KDU Academic Advisor
              </div>
              <div style={{
                fontSize: '11px', color: 'var(--color-text-muted)',
                display: 'none', lineHeight: 1.3,
              }} className="navbar-subtitle">
                Faculty of Computing
              </div>
            </div>
          </button>

          {/* Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>

            {/* Backend status */}
            <div style={{
              display: 'flex', alignItems: 'center', gap: '6px',
              padding: '4px 10px', borderRadius: '20px',
              background: 'var(--color-surface)', border: '1px solid var(--color-border)',
              fontSize: '11px', color: 'var(--color-text-muted)',
            }}>
              <div style={{
                width: '6px', height: '6px', borderRadius: '50%',
                background: backendOnline ? 'var(--color-success)' : 'var(--color-warning)',
                animation: backendOnline ? 'pulse-dot 2s ease-in-out infinite' : 'none',
              }} />
              <span style={{ color: 'var(--color-text-secondary)' }}>
                {backendOnline ? 'API' : 'Offline'}
              </span>
            </div>

            {/* Archetype selector */}
            <select
              aria-label="Load student archetype"
              onChange={(e) => { if (e.target.value) { onLoadDemo(e.target.value); e.target.value = ''; } }}
              defaultValue=""
              style={{
                background: 'var(--color-surface)', border: '1px solid var(--color-border)',
                color: 'var(--color-text-secondary)', fontSize: '12px',
                borderRadius: '8px', padding: '5px 10px', cursor: 'pointer',
                outline: 'none', maxWidth: '170px',
              }}
              className="focus-ring"
            >
              <option value="" disabled>Load archetype...</option>
              {demoProfiles && Object.entries(demoProfiles).map(([k, p]) => (
                <option key={k} value={k} style={{ background: 'var(--color-surface-elevated)' }}>
                  {p.title}
                </option>
              ))}
            </select>

            {/* Reset */}
            <button
              type="button"
              onClick={onReset}
              title="Reset all data"
              aria-label="Reset profile and courses"
              style={{
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                width: '32px', height: '32px', borderRadius: '8px',
                background: 'var(--color-surface)', border: '1px solid var(--color-border)',
                color: 'var(--color-text-muted)', cursor: 'pointer',
                transition: 'all 120ms ease',
              }}
              className="focus-ring reset-btn"
              onMouseEnter={(e) => {
                e.currentTarget.style.color = 'var(--color-danger)';
                e.currentTarget.style.borderColor = 'var(--color-danger-border)';
                e.currentTarget.style.background = 'var(--color-danger-subtle)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = 'var(--color-text-muted)';
                e.currentTarget.style.borderColor = 'var(--color-border)';
                e.currentTarget.style.background = 'var(--color-surface)';
              }}
            >
              <RotateCcw style={{ width: '14px', height: '14px' }} />
            </button>
          </div>
        </div>

        {/* ── Desktop stepper ───────────────────────────────────── */}
        <nav
          aria-label="Academic planning steps"
          style={{
            display: 'flex', alignItems: 'center',
            borderTop: '1px solid var(--color-border-subtle)',
            padding: '10px 0', overflowX: 'auto', gap: '0',
          }}
          className="desktop-stepper"
        >
          {STEPS.map((s, i) => {
            const isActive    = currentStep === s.id;
            const isCompleted = completedSteps.includes(s.id);

            return (
              <React.Fragment key={s.id}>
                <button
                  type="button"
                  onClick={() => setCurrentStep(s.id)}
                  aria-current={isActive ? 'step' : undefined}
                  style={{
                    display: 'flex', alignItems: 'center', gap: '7px',
                    padding: '5px 8px', borderRadius: '8px', border: 'none',
                    cursor: 'pointer', whiteSpace: 'nowrap', flexShrink: 0,
                    transition: 'all 120ms ease',
                    background: isActive ? 'var(--color-primary-subtle)' : 'transparent',
                    outline: 'none',
                  }}
                  className="focus-ring step-btn"
                  data-active={isActive}
                  data-completed={isCompleted}
                >
                  {/* Step number / check circle */}
                  <span style={{
                    width: '20px', height: '20px', borderRadius: '50%',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexShrink: 0, fontSize: '10px', fontWeight: 700,
                    transition: 'all 120ms ease',
                    background: isActive
                      ? 'var(--color-primary)'
                      : isCompleted
                      ? 'var(--color-success-subtle)'
                      : 'var(--color-surface-elevated)',
                    border: isActive
                      ? '1px solid transparent'
                      : isCompleted
                      ? '1px solid var(--color-success-border)'
                      : '1px solid var(--color-border)',
                    color: isActive
                      ? '#fff'
                      : isCompleted
                      ? 'var(--color-success)'
                      : 'var(--color-text-muted)',
                  }}>
                    {isCompleted && !isActive
                      ? <Check style={{ width: '10px', height: '10px' }} />
                      : s.id
                    }
                  </span>

                  {/* Label */}
                  <span style={{
                    fontSize: '12px', fontWeight: isActive ? 600 : isCompleted ? 500 : 400,
                    color: isActive
                      ? 'var(--color-primary)'
                      : isCompleted
                      ? 'var(--color-success)'
                      : 'var(--color-text-muted)',
                    transition: 'color 120ms ease',
                  }}>
                    {s.label}
                  </span>
                </button>

                {/* Connector line */}
                {i < STEPS.length - 1 && (
                  <div style={{
                    flex: 1, height: '1px', minWidth: '16px',
                    background: isCompleted
                      ? 'var(--color-success)'
                      : 'var(--color-border)',
                    opacity: isCompleted ? 0.4 : 1,
                    transition: 'background 200ms ease',
                  }} />
                )}
              </React.Fragment>
            );
          })}
        </nav>

        {/* ── Mobile stepper ────────────────────────────────────── */}
        <div
          style={{
            borderTop: '1px solid var(--color-border-subtle)',
            padding: '10px 0',
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          }}
          className="mobile-stepper"
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-primary)' }}>
              {currentStep}/{STEPS.length}
            </span>
            <span style={{ fontSize: '12px', fontWeight: 500, color: 'var(--color-text-primary)' }}>
              {currentStepObj.label}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            {STEPS.map((s) => (
              <button
                key={s.id}
                type="button"
                onClick={() => setCurrentStep(s.id)}
                aria-label={`Go to step ${s.id}: ${s.label}`}
                style={{
                  height: '3px', borderRadius: '2px', border: 'none', cursor: 'pointer',
                  transition: 'all 150ms ease',
                  width: s.id === currentStep ? '20px' : '6px',
                  background: s.id === currentStep
                    ? 'var(--color-primary)'
                    : completedSteps.includes(s.id)
                    ? 'var(--color-success)'
                    : 'var(--color-border)',
                }}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Responsive visibility CSS */}
      <style>{`
        .desktop-stepper { display: flex !important; }
        .mobile-stepper  { display: none !important; }
        .navbar-subtitle { display: block !important; }

        @media (max-width: 768px) {
          .desktop-stepper { display: none !important; }
          .mobile-stepper  { display: flex !important; }
          .navbar-subtitle { display: none !important; }
        }
      `}</style>
    </header>
  );
}
