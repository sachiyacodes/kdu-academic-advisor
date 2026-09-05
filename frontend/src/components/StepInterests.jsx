import React from 'react';
import { ArrowRight, ArrowLeft, BarChart3, Shield, Code2, X } from 'lucide-react';
import { Button } from './ui';

const PRESETS = [
  {
    label: 'Data Science & AI',
    icon: BarChart3,
    interests: { 'Data Science & Analytics': 5.0, 'Mathematics & Statistics': 4.5, 'Artificial Intelligence': 4.0, 'Database Systems': 3.5 },
  },
  {
    label: 'Cyber Security',
    icon: Shield,
    interests: { 'Cyber Security': 5.0, 'Computer Networks': 4.5, 'Systems & Architecture': 4.0 },
  },
  {
    label: 'Software Engineering',
    icon: Code2,
    interests: { 'Programming & Software Development': 5.0, 'Systems & Architecture': 4.5, 'Database Systems': 4.0, 'Web & Mobile Development': 4.0 },
  },
];

const DESCRIPTORS = [
  [0.0, 'Not selected'],
  [1.5, 'Slight interest'],
  [2.5, 'Moderate'],
  [3.5, 'High interest'],
  [4.5, 'Core passion'],
];

function getDescriptor(val) {
  for (let i = DESCRIPTORS.length - 1; i >= 0; i--) {
    if (val >= DESCRIPTORS[i][0]) return DESCRIPTORS[i][1];
  }
  return 'Not selected';
}

export default function StepInterests({ interests, setInterests, catalogInterests, onPrev, onNext }) {
  const activeCount = Object.keys(interests).length;

  const handleChange = (area, value) => {
    const val = parseFloat(value);
    if (val === 0) {
      const u = { ...interests };
      delete u[area];
      setInterests(u);
    } else {
      setInterests({ ...interests, [area]: val });
    }
  };

  return (
    <div className="animate-fadeIn" style={{ maxWidth: '800px', margin: '0 auto' }}>

      {/* ── Header ───────────────────────────────────────────────── */}
      <div style={{
        padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '24px',
      }}>
        <div>
          <h1 style={{ fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em', color: 'var(--color-text-primary)', margin: 0, lineHeight: 1.3 }}>
            Career Interests
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: '6px 0 0', lineHeight: 1.6 }}>
            Rate your interest in each subject area from 0 to 5. The hybrid engine weights these alongside your academic performance.
          </p>
        </div>
        <div style={{
          display: 'flex', alignItems: 'center', gap: '8px',
          background: 'var(--color-surface)', border: '1px solid var(--color-border)',
          borderRadius: '8px', padding: '8px 14px', flexShrink: 0,
        }}>
          <span style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>Active</span>
          <span style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-primary)', fontVariantNumeric: 'tabular-nums' }}>
            {activeCount}<span style={{ fontSize: '12px', fontWeight: 400, color: 'var(--color-text-muted)' }}>/{catalogInterests.length}</span>
          </span>
        </div>
      </div>

      {/* ── Presets ──────────────────────────────────────────────── */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', padding: '16px 0', borderBottom: '1px solid var(--color-border-subtle)' }}>
        <span style={{ fontSize: '11px', color: 'var(--color-text-muted)', alignSelf: 'center', marginRight: '4px' }}>Presets:</span>
        {PRESETS.map(({ label, icon: Icon, interests: preset }) => (
          <button
            key={label}
            type="button"
            onClick={() => setInterests(preset)}
            style={{
              display: 'flex', alignItems: 'center', gap: '6px',
              padding: '5px 12px', borderRadius: '8px',
              background: 'var(--color-surface)', border: '1px solid var(--color-border)',
              color: 'var(--color-text-secondary)', fontSize: '12px', fontWeight: 500,
              cursor: 'pointer', transition: 'all 120ms ease',
            }}
            className="focus-ring"
            onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'var(--color-primary-border)'; e.currentTarget.style.color = 'var(--color-primary)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'var(--color-border)'; e.currentTarget.style.color = 'var(--color-text-secondary)'; }}
          >
            <Icon style={{ width: '12px', height: '12px' }} />
            {label}
          </button>
        ))}
        {activeCount > 0 && (
          <button
            type="button"
            onClick={() => setInterests({})}
            style={{
              display: 'flex', alignItems: 'center', gap: '4px',
              padding: '5px 10px', borderRadius: '8px',
              background: 'none', border: '1px solid transparent',
              color: 'var(--color-text-muted)', fontSize: '11px', fontWeight: 500,
              cursor: 'pointer', transition: 'all 120ms ease', marginLeft: 'auto',
            }}
            className="focus-ring"
            onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--color-danger)'; }}
            onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--color-text-muted)'; }}
          >
            <X style={{ width: '11px', height: '11px' }} /> Clear all
          </button>
        )}
      </div>

      {/* ── Interest list ─────────────────────────────────────────── */}
      {/* Two-column layout — each item is a horizontal row with slider */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0', marginTop: '4px' }} className="interests-grid">
        {catalogInterests.map((item, idx) => {
          const area = item.subject_area || item.name;
          const val = interests[area] || 0;
          const active = val > 0;
          const desc = getDescriptor(val);
          const pct = (val / 5) * 100;

          return (
            <div
              key={item.interest_id}
              style={{
                padding: '14px 16px',
                borderBottom: '1px solid var(--color-border-subtle)',
                borderRight: idx % 2 === 0 ? '1px solid var(--color-border-subtle)' : 'none',
                transition: 'background 120ms ease',
                background: active ? 'var(--color-primary-subtle)' : 'transparent',
              }}
            >
              {/* Label row */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                <span style={{
                  fontSize: '12px', fontWeight: active ? 600 : 500,
                  color: active ? 'var(--color-text-primary)' : 'var(--color-text-secondary)',
                  transition: 'color 120ms ease',
                }}>
                  {item.name}
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{
                    fontSize: '11px', fontWeight: 500,
                    color: active ? 'var(--color-primary)' : 'var(--color-text-muted)',
                  }}>
                    {active ? val.toFixed(1) : '—'}
                  </span>
                  <span style={{
                    fontSize: '10px',
                    color: active ? 'var(--color-text-secondary)' : 'var(--color-text-disabled)',
                    minWidth: '72px', textAlign: 'right',
                  }}>
                    {desc}
                  </span>
                </div>
              </div>

              {/* Slider */}
              <input
                type="range" min="0" max="5" step="0.5" value={val}
                aria-label={`Interest in ${item.name}`}
                onChange={(e) => handleChange(area, e.target.value)}
                className="interest-slider"
                style={{
                  background: `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${pct}%, var(--color-border) ${pct}%, var(--color-border) 100%)`,
                }}
              />
            </div>
          );
        })}
      </div>

      {/* ── Navigation ───────────────────────────────────────────── */}
      <div style={{ paddingTop: '20px', borderTop: '1px solid var(--color-border-subtle)', display: 'flex', justifyContent: 'space-between', marginTop: '4px' }}>
        <Button variant="secondary" size="md" icon={ArrowLeft} onClick={onPrev}>Courses</Button>
        <Button variant="primary" size="lg" icon={ArrowRight} iconPosition="right" onClick={onNext}>Generate recommendations</Button>
      </div>

      <style>{`
        @media (max-width: 640px) {
          .interests-grid { grid-template-columns: 1fr !important; }
          .interests-grid > div { border-right: none !important; }
        }
      `}</style>
    </div>
  );
}
