import React from 'react';
import {
  GraduationCap,
  Check,
  AlertTriangle,
  BarChart3,
  ArrowLeft,
  RotateCcw,
  BookOpen,
  Info,
} from 'lucide-react';
import { Card, Button, Progress, Skeleton } from './ui';

export default function StepGraduation({
  auditData,
  recData,
  loading,
  onPrev,
  onReset,
}) {
  if (loading) {
    return (
      <div className="space-y-6 md:space-y-8 animate-fadeIn">
        <div className="border-b border-border pb-5 space-y-2">
          <Skeleton className="h-4 w-28" />
          <Skeleton className="h-8 w-80" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Skeleton className="h-20 w-full" />
          <Skeleton className="h-20 w-full" />
          <Skeleton className="h-20 w-full" />
          <Skeleton className="h-20 w-full" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Skeleton className="h-36 w-full" />
          <Skeleton className="h-36 w-full" />
        </div>
      </div>
    );
  }

  if (!auditData) {
    return (
      <Card className="py-16 text-center space-y-4 max-w-lg mx-auto">
        <AlertTriangle className="w-10 h-10 text-warning mx-auto" />
        <h2 className="text-base font-semibold text-text-primary">No Audit Data Available</h2>
        <Button variant="primary" size="md" onClick={onPrev}>
          Back to Elective Advisor
        </Button>
      </Card>
    );
  }

  const {
    gpa,
    classification,
    core_credits = 0,
    elective_credits = 0,
    gpa_credits_earned = 0,
    gpa_target = 120,
    gpa_progress_pct = 0,
    ngpa_credits_earned = 0,
    ngpa_target = 14,
    ngpa_progress_pct = 0,
    total_credits_earned = 0,
    is_eligible = false,
    bottlenecks = [],
  } = auditData;

  const profile = recData?.profile;
  const subjectPerfs = profile?.subject_performances || [];

  return (
    <div className="space-y-6 md:space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-border pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-primary text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 6 of 6 · Degree Completion Audit</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-primary tracking-tight">
            Graduation Credit Audit & Analytics
          </h1>
          <p className="text-sm text-text-secondary mt-1">
            Evaluation against official degree requirements: 120 GPA credits and 14 NGPA credits.
          </p>
        </div>

        {/* Graduation Clearance Status Banner */}
        <Card
          padding="sm"
          className={`flex items-center space-x-3 px-4 shrink-0 shadow-xs ${
            is_eligible ? 'border-success-border bg-success-subtle' : 'border-border'
          }`}
        >
          <div
            className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${
              is_eligible ? 'bg-success text-white' : 'bg-primary-subtle text-primary border border-primary-border'
            }`}
          >
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-semibold text-text-secondary block tracking-wider">
              Graduation Clearance
            </span>
            <strong className={`text-xs font-bold ${is_eligible ? 'text-success' : 'text-text-primary'}`}>
              {is_eligible ? 'All Graduation Requirements Met' : 'Degree In Progress'}
            </strong>
          </div>
        </Card>
      </div>

      {/* Academic Standing Summary Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card padding="sm" className="space-y-1">
          <span className="text-[10px] uppercase font-semibold text-text-muted block tracking-wider">
            Academic Stage
          </span>
          <span className="text-sm font-bold text-text-primary block">
            {profile ? `Year ${profile.year}, Sem ${profile.semester}` : 'Enrolled'}
          </span>
        </Card>

        <Card padding="sm" className="space-y-1">
          <span className="text-[10px] uppercase font-semibold text-text-muted block tracking-wider">
            Cumulative GPA
          </span>
          <span className="text-sm font-bold text-primary block">
            {gpa ? gpa.toFixed(2) : '0.00'}
          </span>
        </Card>

        <Card padding="sm" className="space-y-1">
          <span className="text-[10px] uppercase font-semibold text-text-muted block tracking-wider">
            Classification
          </span>
          <span className="text-sm font-bold text-success block truncate">
            {classification || 'Good Standing'}
          </span>
        </Card>

        <Card padding="sm" className="space-y-1">
          <span className="text-[10px] uppercase font-semibold text-text-muted block tracking-wider">
            Total Credits Earned
          </span>
          <span className="text-sm font-bold text-text-primary block">
            {total_credits_earned || gpa_credits_earned + ngpa_credits_earned} cr
          </span>
        </Card>
      </div>

      {/* Credit Progress Gauges */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* GPA Credits Card */}
        <Card className="space-y-4 shadow-xs">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-xs font-semibold text-text-primary block">
                Core & Elective GPA Credits
              </span>
              <p className="text-[11px] text-text-secondary mt-0.5">
                Core: <strong className="text-text-primary">{core_credits}</strong> cr · Elective: <strong className="text-text-primary">{elective_credits}</strong> cr
              </p>
            </div>
            <div className="text-right">
              <span className="text-xl font-black text-text-primary">{gpa_credits_earned}</span>
              <span className="text-xs text-text-muted font-medium"> / {gpa_target}</span>
            </div>
          </div>

          <div className="space-y-2">
            <Progress
              value={gpa_progress_pct}
              max={100}
              variant="primary"
              size="md"
            />
            <div className="flex justify-between text-[11px] text-text-secondary">
              <span className="font-semibold text-primary">{gpa_progress_pct}% Complete</span>
              <span>{Math.max(0, gpa_target - gpa_credits_earned)} credits remaining</span>
            </div>
          </div>
        </Card>

        {/* NGPA Credits Card */}
        <Card className="space-y-4 shadow-xs">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-xs font-semibold text-text-primary block">
                Non-GPA (NGPA) Auxiliary Credits
              </span>
              <p className="text-[11px] text-text-secondary mt-0.5">
                English, Industrial Internship, and Leadership modules
              </p>
            </div>
            <div className="text-right">
              <span className="text-xl font-black text-text-primary">{ngpa_credits_earned}</span>
              <span className="text-xs text-text-muted font-medium"> / {ngpa_target}</span>
            </div>
          </div>

          <div className="space-y-2">
            <Progress
              value={ngpa_progress_pct}
              max={100}
              variant="teal"
              size="md"
            />
            <div className="flex justify-between text-[11px] text-text-secondary">
              <span className="font-semibold text-teal">{ngpa_progress_pct}% Complete</span>
              <span>{Math.max(0, ngpa_target - ngpa_credits_earned)} credits remaining</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Curriculum & Benchmark Information Notice */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-xs">
        <Card padding="sm" className="space-y-1">
          <div className="flex items-center space-x-1.5 font-semibold text-text-primary">
            <BookOpen className="w-3.5 h-3.5 text-primary" />
            <span>KDU Electives Policy</span>
          </div>
          <p className="text-text-secondary text-[11px] leading-relaxed">
            In the KDU computing curriculum, elective options begin in <strong>Year 3, Semester 2</strong> and extend into Year 4. Modules in Years 1 & 2 are mandatory degree core foundations.
          </p>
        </Card>

        <Card padding="sm" className="space-y-1">
          <div className="flex items-center space-x-1.5 font-semibold text-text-primary">
            <Info className="w-3.5 h-3.5 text-teal" />
            <span>Stage-Aware Verification</span>
          </div>
          <p className="text-text-secondary text-[11px] leading-relaxed">
            Transcript evaluations dynamically incorporate all completed prior courses ({gpa_credits_earned} GPA credits, {ngpa_credits_earned} NGPA credits). You can adjust any grade in <strong>Step 2</strong>.
          </p>
        </Card>
      </div>

      {/* Prerequisite Bottlenecks Alert */}
      {bottlenecks.length > 0 ? (
        <Card className="border-warning-border bg-warning-subtle space-y-2.5">
          <div className="flex items-center space-x-2 text-warning font-semibold text-xs uppercase tracking-wider">
            <AlertTriangle className="w-4 h-4" />
            <span>Prerequisite Bottlenecks Detected</span>
          </div>
          <p className="text-xs text-text-primary leading-relaxed">
            The following courses serve as prerequisite foundations for multiple upcoming subjects. Completing them is essential to prevent curriculum progression delays:
          </p>
          <ul className="space-y-1 text-xs text-text-secondary list-disc list-inside">
            {bottlenecks.map((b, i) => (
              <li key={i} className="leading-relaxed font-medium">
                {b}
              </li>
            ))}
          </ul>
        </Card>
      ) : (
        <Card className="border-success-border bg-success-subtle flex items-center space-x-3 p-4">
          <div className="w-8 h-8 rounded-full bg-success/20 flex items-center justify-center text-success shrink-0">
            <Check className="w-4 h-4" />
          </div>
          <div>
            <strong className="block text-xs font-semibold text-text-primary">
              No Prerequisite Bottlenecks
            </strong>
            <span className="text-xs text-text-secondary">
              All prerequisite chains for your current curriculum stage are satisfied.
            </span>
          </div>
        </Card>
      )}

      {/* Subject Area Performance Distribution */}
      {subjectPerfs.length > 0 && (
        <Card className="space-y-4 shadow-xs">
          <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
            <h3 className="text-sm font-semibold text-text-primary flex items-center space-x-2">
              <BarChart3 className="w-4 h-4 text-primary" />
              <span>Academic Performance by Subject Taxonomy Area</span>
            </h3>
            <span className="text-xs text-text-muted font-medium">
              Taxonomy Areas: <strong className="text-primary">{subjectPerfs.length}</strong>
            </span>
          </div>

          <div className="space-y-3 pt-1">
            {subjectPerfs.map((p) => {
              const mark = p.average_mark;
              let variant = 'primary';
              if (mark >= 80) variant = 'success';
              else if (mark < 55) variant = 'warning';

              const courseCountText =
                p.course_count === 1 ? '1 course' : `${p.course_count} courses`;

              return (
                <div key={p.subject_area} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-text-primary font-medium">{p.subject_area}</span>
                    <span className="font-mono text-text-secondary font-semibold">
                      {mark.toFixed(1)}% <span className="text-text-muted font-normal">({courseCountText})</span>
                    </span>
                  </div>
                  <div className="w-full h-1.5 bg-border rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-300 ${
                        variant === 'success'
                          ? 'bg-success'
                          : variant === 'warning'
                          ? 'bg-warning'
                          : 'bg-primary'
                      }`}
                      style={{ width: `${Math.min(100, mark)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Footer Controls */}
      <div className="pt-6 border-t border-border flex items-center justify-between">
        <Button
          variant="secondary"
          size="md"
          icon={ArrowLeft}
          onClick={onPrev}
        >
          Back to Elective Advisor
        </Button>

        <Button
          variant="secondary"
          size="md"
          icon={RotateCcw}
          onClick={onReset}
        >
          Reset & Start New Evaluation
        </Button>
      </div>
    </div>
  );
}
