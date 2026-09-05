import React from 'react';
import { Sparkles, ArrowRight, ArrowLeft, BarChart3, Shield, Code2 } from 'lucide-react';
import { Card, Button, Badge } from './ui';

export default function StepInterests({
  interests,
  setInterests,
  catalogInterests,
  onPrev,
  onNext,
}) {
  const activeCount = Object.keys(interests).length;

  const handleIntensityChange = (subjectArea, value) => {
    const val = parseFloat(value);
    if (val === 0) {
      const updated = { ...interests };
      delete updated[subjectArea];
      setInterests(updated);
    } else {
      setInterests({ ...interests, [subjectArea]: val });
    }
  };

  const applyPreset = (presetMap) => {
    setInterests(presetMap);
  };

  return (
    <div className="space-y-6 md:space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-border pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-primary text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 3 of 6</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-primary tracking-tight">
            Career Interests & Preferences
          </h1>
          <p className="text-sm text-text-secondary mt-1">
            Calibrate your personal aspirations. The hybrid engine balances your interest weights (1.0 – 5.0) alongside course performances.
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-surface border border-border rounded-xl px-4 py-2 text-xs shrink-0">
          <span className="text-text-secondary">Active Interests:</span>
          <span className="font-bold text-primary">{activeCount} / {catalogInterests.length}</span>
        </div>
      </div>

      {/* Quick Presets Banner */}
      <Card padding="sm" className="space-y-3">
        <div className="flex items-center space-x-2 text-xs font-semibold text-text-primary">
          <Sparkles className="w-3.5 h-3.5 text-teal" />
          <span>Quick Alignment Presets:</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            variant="secondary"
            size="sm"
            icon={BarChart3}
            onClick={() =>
              applyPreset({
                'Data Science & Analytics': 5.0,
                'Mathematics & Statistics': 4.5,
                'Artificial Intelligence': 4.0,
                'Database Systems': 3.5,
              })
            }
          >
            Data Science & AI Focus
          </Button>

          <Button
            variant="secondary"
            size="sm"
            icon={Shield}
            onClick={() =>
              applyPreset({
                'Cyber Security': 5.0,
                'Computer Networks': 4.5,
                'Systems & Architecture': 4.0,
              })
            }
          >
            Cyber Security & Networks
          </Button>

          <Button
            variant="secondary"
            size="sm"
            icon={Code2}
            onClick={() =>
              applyPreset({
                'Programming & Software Development': 5.0,
                'Systems & Architecture': 4.5,
                'Database Systems': 4.0,
                'Web & Mobile Development': 4.0,
              })
            }
          >
            Software Engineering
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => setInterests({})}
            className="text-text-muted hover:text-danger"
          >
            Clear All
          </Button>
        </div>
      </Card>

      {/* Interests Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {catalogInterests.map((item) => {
          const area = item.subject_area || item.name;
          const currentIntensity = interests[area] || 0;
          const isSelected = currentIntensity > 0;

          const getDescriptor = (val) => {
            if (val === 0) return 'Not Selected';
            if (val >= 4.5) return 'Core Passion';
            if (val >= 3.5) return 'High Interest';
            if (val >= 2.5) return 'Moderate';
            return 'Slight Interest';
          };

          return (
            <Card
              key={item.interest_id}
              className={`flex flex-col justify-between space-y-4 transition-all duration-150 ${
                isSelected
                  ? 'border-primary/40 bg-surface shadow-xs'
                  : 'bg-surface/60 hover:border-border'
              }`}
            >
              <div>
                <div className="flex items-start justify-between gap-2">
                  <h3 className="text-xs font-semibold text-text-primary">
                    {item.name}
                  </h3>
                  {isSelected && (
                    <Badge variant="primary" size="sm">
                      {currentIntensity.toFixed(1)} / 5.0
                    </Badge>
                  )}
                </div>
                <p className="text-[11px] text-text-secondary mt-1.5 line-clamp-2 leading-relaxed">
                  {item.description || `Explore concepts and applied technologies in ${area}`}
                </p>
              </div>

              {/* Slider Control */}
              <div className="space-y-1.5 pt-3 border-t border-border-subtle">
                <div className="flex justify-between text-[11px]">
                  <span className="text-text-muted">None (0)</span>
                  <span className={isSelected ? 'text-primary font-semibold' : 'text-text-muted'}>
                    {getDescriptor(currentIntensity)}
                  </span>
                  <span className="text-text-muted">Max (5.0)</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="5"
                  step="0.5"
                  value={currentIntensity}
                  aria-label={`Interest intensity for ${item.name}`}
                  onChange={(e) => handleIntensityChange(area, e.target.value)}
                  className="w-full h-1.5 bg-border rounded-full appearance-none cursor-pointer focus-ring accent-primary"
                  style={{
                    background: `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${
                      (currentIntensity / 5) * 100
                    }%, var(--color-border) ${(currentIntensity / 5) * 100}%, var(--color-border) 100%)`,
                  }}
                />
              </div>
            </Card>
          );
        })}
      </div>

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-border flex items-center justify-between">
        <Button
          variant="secondary"
          size="md"
          icon={ArrowLeft}
          onClick={onPrev}
        >
          Back to Course History
        </Button>

        <Button
          variant="primary"
          size="lg"
          icon={ArrowRight}
          iconPosition="right"
          onClick={onNext}
        >
          Generate Recommendations
        </Button>
      </div>
    </div>
  );
}
