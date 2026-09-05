import React from 'react';
import { BookOpen, Calendar, Sparkles, ArrowRight, School, Info } from 'lucide-react';
import { Card, Button, Badge } from './ui';

export default function StepProfile({
  profile,
  setProfile,
  degrees,
  demoProfiles,
  onLoadDemo,
  onNext,
}) {
  return (
    <div className="space-y-6 md:space-y-8 animate-fadeIn">
      {/* Page Header */}
      <div className="border-b border-border pb-5">
        <div className="flex items-center space-x-2 text-primary text-xs font-semibold uppercase tracking-wider mb-1">
          <span>Step 1 of 6</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-text-primary tracking-tight">
          Academic Profile Setup
        </h1>
        <p className="text-sm text-text-secondary mt-1 max-w-3xl leading-relaxed">
          Configure your enrolled degree program and current academic standing. You can also load
          a benchmark student archetype to immediately test the recommendation pipeline.
        </p>
      </div>

      {/* Main Form & Benchmark Archetypes Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
        {/* Left 2 Cols: Profile Form */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="space-y-6">
            <div className="flex items-center space-x-2.5 pb-3 border-b border-border-subtle">
              <div className="w-8 h-8 rounded-lg bg-primary-subtle border border-primary-border flex items-center justify-center text-primary shrink-0">
                <School className="w-4 h-4" />
              </div>
              <h2 className="text-base font-semibold text-text-primary">
                Degree & Academic Standing
              </h2>
            </div>

            {/* Degree Select */}
            <div className="space-y-2">
              <label htmlFor="degree-select" className="block text-xs font-semibold text-text-secondary">
                Enrolled Degree Program
              </label>
              <select
                id="degree-select"
                value={profile.degree}
                onChange={(e) => setProfile({ ...profile, degree: e.target.value })}
                className="w-full h-11 bg-bg-secondary border border-border rounded-lg px-3.5 py-2 text-sm text-text-primary focus-ring transition cursor-pointer"
              >
                {degrees.map((d) => {
                  const degName = d.name || d.degree_name;
                  return (
                    <option key={d.degree_id} value={degName} className="bg-surface text-text-primary">
                      {degName}
                    </option>
                  );
                })}
              </select>
              {profile.degree === 'Custom / Other University Degree' && (
                <div className="flex items-start space-x-2 text-xs text-text-primary bg-info-subtle border border-info/30 rounded-lg p-3 mt-2">
                  <Info className="w-4 h-4 text-info shrink-0 mt-0.5" />
                  <div className="leading-relaxed">
                    <strong className="font-semibold text-info">Universal Curriculum Mode:</strong> Enables manual course entry from any institution and unlocks exploration of all 89 electives across computing departments.
                  </div>
                </div>
              )}
            </div>

            {/* Year & Semester Controls */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Academic Year */}
              <div className="space-y-2">
                <label className="block text-xs font-semibold text-text-secondary flex items-center space-x-1.5">
                  <Calendar className="w-3.5 h-3.5 text-primary" />
                  <span>Current Academic Year</span>
                </label>
                <div className="grid grid-cols-4 gap-2">
                  {[1, 2, 3, 4].map((y) => {
                    const isSelected = profile.year === y;
                    return (
                      <button
                        key={y}
                        type="button"
                        onClick={() => setProfile({ ...profile, year: y })}
                        aria-pressed={isSelected}
                        className={`h-11 rounded-lg text-xs font-semibold transition-all duration-150 cursor-pointer focus-ring ${
                          isSelected
                            ? 'bg-primary text-white shadow-xs border border-primary/20'
                            : 'bg-bg-secondary text-text-secondary hover:text-text-primary hover:bg-surface-hover border border-border'
                        }`}
                      >
                        Year {y}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Semester */}
              <div className="space-y-2">
                <label className="block text-xs font-semibold text-text-secondary flex items-center space-x-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-primary" />
                  <span>Current Semester</span>
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {[1, 2].map((s) => {
                    const isSelected = profile.semester === s;
                    return (
                      <button
                        key={s}
                        type="button"
                        onClick={() => setProfile({ ...profile, semester: s })}
                        aria-pressed={isSelected}
                        className={`h-11 rounded-lg text-xs font-semibold transition-all duration-150 cursor-pointer focus-ring ${
                          isSelected
                            ? 'bg-primary text-white shadow-xs border border-primary/20'
                            : 'bg-bg-secondary text-text-secondary hover:text-text-primary hover:bg-surface-hover border border-border'
                        }`}
                      >
                        Semester {s}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Form Footer Action */}
            <div className="pt-4 border-t border-border-subtle flex justify-end">
              <Button
                variant="primary"
                size="lg"
                onClick={onNext}
                icon={ArrowRight}
                iconPosition="right"
              >
                Proceed to Course History
              </Button>
            </div>
          </Card>
        </div>

        {/* Right 1 Col: Benchmark Archetypes */}
        <div className="space-y-4">
          <Card className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <div className="flex items-center space-x-2 font-semibold text-sm text-text-primary">
                <Sparkles className="w-4 h-4 text-teal" />
                <span>Benchmark Archetypes</span>
              </div>
              <Badge variant="teal" size="sm">
                Stage: Y{profile.year}S{profile.semester}
              </Badge>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              Loads pre-configured student marks and interests adapted to your selected stage. Autofills completed courses prior to <strong className="text-text-primary">Year {profile.year} Sem {profile.semester}</strong>:
            </p>

            <div className="space-y-2 pt-1">
              {demoProfiles &&
                Object.entries(demoProfiles).map(([key, demo]) => (
                  <button
                    key={key}
                    type="button"
                    onClick={() => onLoadDemo(key)}
                    className="w-full text-left p-3 rounded-lg bg-bg-secondary hover:bg-surface-hover border border-border hover:border-primary/40 transition-all duration-150 group cursor-pointer focus-ring"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold text-text-primary group-hover:text-primary transition-colors">
                        {demo.title.split('—')[0].trim()}
                      </span>
                      <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-surface border border-border text-text-secondary group-hover:bg-primary-subtle group-hover:text-primary group-hover:border-primary-border transition-colors">
                        Load
                      </span>
                    </div>
                    <p className="text-[11px] text-text-muted group-hover:text-text-secondary mt-1 line-clamp-2 leading-relaxed transition-colors">
                      {demo.description}
                    </p>
                  </button>
                ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
