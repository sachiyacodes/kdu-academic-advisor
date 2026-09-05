import React from 'react';
import { GraduationCap, RotateCcw, Sparkles, Check } from 'lucide-react';
import Badge from './ui/Badge';
import IconButton from './ui/IconButton';

export default function Navbar({
  currentStep,
  setCurrentStep,
  completedSteps,
  demoProfiles,
  onLoadDemo,
  onReset,
  backendOnline,
}) {
  const steps = [
    { id: 1, label: 'Profile' },
    { id: 2, label: 'Courses' },
    { id: 3, label: 'Interests' },
    { id: 4, label: 'Recommendations' },
    { id: 5, label: 'Electives' },
    { id: 6, label: 'Graduation' },
  ];

  const currentStepObj = steps.find((s) => s.id === currentStep) || steps[0];

  return (
    <header className="border-b border-border bg-bg-secondary/95 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Top Header Row */}
        <div className="flex items-center justify-between h-16">
          {/* Brand Mark & Academic Meta */}
          <div
            className="flex items-center space-x-3 cursor-pointer select-none focus-ring rounded-lg p-1 -ml-1"
            onClick={() => setCurrentStep(1)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && setCurrentStep(1)}
            aria-label="Go to Step 1: Student Profile"
          >
            <div className="w-9 h-9 rounded-lg bg-primary-subtle border border-primary-border flex items-center justify-center text-primary shrink-0 shadow-xs">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-base text-text-primary tracking-tight">
                  KDU Academic Advisor
                </span>
                <Badge variant="teal" size="sm" icon={Sparkles}>
                  Advisor
                </Badge>
              </div>
              <p className="text-xs text-text-secondary hidden sm:block">
                Faculty of Computing · IT3182 Essentials of AI
              </p>
            </div>
          </div>

          {/* Header Controls: System Status, Archetype Selector, Reset */}
          <div className="flex items-center space-x-2.5">
            {/* Backend Connectivity Status */}
            <div
              className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-surface border border-border text-xs"
              title={backendOnline ? 'Backend service online' : 'Backend service unreachable'}
            >
              <div
                className={`w-2 h-2 rounded-full ${
                  backendOnline ? 'bg-success animate-pulse' : 'bg-warning'
                }`}
              />
              <span className="text-text-secondary text-xs">
                {backendOnline ? 'API Connected' : 'Connecting...'}
              </span>
            </div>

            {/* Quick Demo Archetype Selector */}
            <div className="relative inline-block">
              <select
                aria-label="Load benchmark student archetype"
                onChange={(e) => {
                  if (e.target.value) {
                    onLoadDemo(e.target.value);
                    e.target.value = '';
                  }
                }}
                defaultValue=""
                className="bg-surface hover:bg-surface-hover border border-border text-text-primary text-xs rounded-lg px-3 py-1.5 focus-ring cursor-pointer transition font-medium"
              >
                <option value="" disabled>
                  Load Student Archetype...
                </option>
                {demoProfiles &&
                  Object.entries(demoProfiles).map(([k, p]) => (
                    <option key={k} value={k} className="bg-surface-elevated text-text-primary">
                      {p.title}
                    </option>
                  ))}
              </select>
            </div>

            {/* Reset State Button */}
            <IconButton
              icon={RotateCcw}
              label="Reset profile and courses"
              variant="destructive"
              size="sm"
              onClick={onReset}
            />
          </div>
        </div>

        {/* Responsive Stepper: Desktop & Tablet */}
        <nav
          aria-label="Academic planning steps"
          className="hidden md:flex items-center justify-between border-t border-border-subtle py-2.5 overflow-x-auto"
        >
          {steps.map((s) => {
            const isActive = currentStep === s.id;
            const isCompleted = completedSteps.includes(s.id);
            return (
              <button
                key={s.id}
                type="button"
                onClick={() => setCurrentStep(s.id)}
                aria-current={isActive ? 'step' : undefined}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs transition whitespace-nowrap cursor-pointer focus-ring ${
                  isActive
                    ? 'bg-primary-subtle text-primary border border-primary-border font-semibold shadow-xs'
                    : isCompleted
                    ? 'text-success hover:bg-surface hover:text-success font-medium'
                    : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover'
                }`}
              >
                <span
                  className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0 ${
                    isActive
                      ? 'bg-primary text-white'
                      : isCompleted
                      ? 'bg-success-subtle text-success border border-success-border'
                      : 'bg-surface-elevated text-text-secondary border border-border'
                  }`}
                >
                  {isCompleted && !isActive ? <Check className="w-3 h-3" /> : s.id}
                </span>
                <span>{s.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Responsive Mobile Stepper (< 768px) */}
        <div className="md:hidden border-t border-border-subtle py-2.5 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-primary">
              Step {currentStep} of {steps.length}:
            </span>
            <span className="text-text-primary font-medium">{currentStepObj.label}</span>
          </div>
          <div className="flex items-center space-x-1">
            {steps.map((s) => (
              <button
                key={s.id}
                type="button"
                onClick={() => setCurrentStep(s.id)}
                aria-label={`Go to step ${s.id}: ${s.label}`}
                className={`h-1.5 rounded-full transition-all cursor-pointer ${
                  s.id === currentStep
                    ? 'w-6 bg-primary'
                    : completedSteps.includes(s.id)
                    ? 'w-2 bg-success'
                    : 'w-2 bg-border'
                }`}
              />
            ))}
          </div>
        </div>
      </div>
    </header>
  );
}
