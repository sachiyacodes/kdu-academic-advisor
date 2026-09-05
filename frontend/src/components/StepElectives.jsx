import React, { useState } from 'react';
import {
  Compass,
  Check,
  AlertCircle,
  Clock,
  Unlock,
  Layers,
  ArrowRight,
  ArrowLeft,
} from 'lucide-react';
import { Card, Button, Badge, Tabs, Skeleton } from './ui';

export default function StepElectives({
  advisorData,
  loading,
  targetSpec,
  setTargetSpec,
  specializations,
  onPrev,
  onNext,
}) {
  const [activeTab, setActiveTab] = useState('electives');

  if (loading) {
    return (
      <div className="space-y-6 md:space-y-8 animate-fadeIn">
        <div className="border-b border-border pb-5 space-y-2">
          <Skeleton className="h-4 w-28" />
          <Skeleton className="h-8 w-80" />
          <Skeleton className="h-4 w-96" />
        </div>
        <Skeleton className="h-12 w-96" />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Skeleton className="h-36 w-full" />
          <Skeleton className="h-36 w-full" />
          <Skeleton className="h-36 w-full" />
          <Skeleton className="h-36 w-full" />
        </div>
      </div>
    );
  }

  if (!advisorData) {
    return (
      <Card className="py-16 text-center space-y-4 max-w-lg mx-auto">
        <AlertCircle className="w-10 h-10 text-warning mx-auto" />
        <h2 className="text-base font-semibold text-text-primary">No Advisor Data Available</h2>
        <Button variant="primary" size="md" onClick={onPrev}>
          Back to Recommendations
        </Button>
      </Card>
    );
  }

  const { electives = [], core_courses = [], roadmap = {} } = advisorData;

  const recNow = electives.filter((e) => e.category === 'Recommended Now');
  const recLater = electives.filter((e) => e.category === 'Recommended Later');

  const tabList = [
    { id: 'electives', label: 'Personalized Electives', count: electives.length, icon: Compass },
    { id: 'cores', label: 'Core Degree Pathways', count: core_courses.length, icon: Layers },
    { id: 'roadmap', label: '4-Year Curriculum Roadmap', icon: Clock },
  ];

  return (
    <div className="space-y-6 md:space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-border pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-primary text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 5 of 6 · Rule-Based Advisor</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-primary tracking-tight">
            Elective Advisor & Degree Roadmap
          </h1>
          <p className="text-sm text-text-secondary mt-1">
            Prerequisite validation, stage eligibility checks, and specialization synergy calibration.
          </p>
        </div>

        {/* Target Specialization Selector */}
        <Card padding="sm" className="space-y-1 shrink-0">
          <label htmlFor="target-spec-select" className="text-[10px] uppercase font-semibold text-text-secondary block tracking-wider">
            Target Pathway for Synergy Scoring:
          </label>
          <select
            id="target-spec-select"
            value={targetSpec}
            onChange={(e) => setTargetSpec(e.target.value)}
            className="w-full bg-bg-secondary border border-border text-xs text-primary font-semibold rounded-lg px-3 py-1.5 focus-ring cursor-pointer"
          >
            {specializations &&
              specializations.map((s) => (
                <option key={s.specialization_id} value={s.name} className="bg-surface text-text-primary">
                  {s.name}
                </option>
              ))}
          </select>
        </Card>
      </div>

      {/* Segmented Tabs Control */}
      <div>
        <Tabs
          tabs={tabList}
          activeTab={activeTab}
          onChange={setActiveTab}
        />
      </div>

      {/* Tab 1: Electives */}
      {activeTab === 'electives' && (
        <div className="space-y-6">
          {/* Section: Recommended Now */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h2 className="text-xs font-semibold uppercase tracking-wider text-success flex items-center space-x-1.5">
                <Check className="w-4 h-4" />
                <span>Recommended Now ({recNow.length}) — Prerequisites Met & Stage Eligible</span>
              </h2>
            </div>

            {recNow.length === 0 ? (
              <Card className="p-6 text-center text-xs text-text-muted italic border-dashed">
                No electives currently eligible for immediate enrollment. Check prerequisites in Recommended Later below.
              </Card>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                {recNow.map((item) => (
                  <Card
                    key={item.course.course_code}
                    className="border-l-4 border-l-success space-y-3 shadow-xs hover:border-border"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center space-x-2">
                          <span className="text-xs font-mono font-bold text-success">
                            {item.course.course_code}
                          </span>
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-surface-elevated text-text-secondary border border-border">
                            {item.course.credits} cr · Y{item.course.year} S{item.course.semester}
                          </span>
                        </div>
                        <h3 className="text-xs font-semibold text-text-primary mt-1">
                          {item.course.course_name}
                        </h3>
                        <p className="text-[11px] text-text-muted mt-0.5">{item.course.subject_area}</p>
                      </div>

                      <div className="text-right shrink-0">
                        <span className="text-[10px] uppercase font-semibold text-text-muted block">
                          Synergy
                        </span>
                        <span className="text-base font-black text-primary">
                          {item.synergy_score}%
                        </span>
                      </div>
                    </div>

                    <p className="text-xs text-text-secondary bg-bg-secondary rounded-lg p-2.5 border border-border-subtle leading-relaxed">
                      {item.reason}
                    </p>

                    {item.chain_impact_count > 0 && (
                      <div className="text-[11px] text-warning flex items-center space-x-1.5 font-medium">
                        <Unlock className="w-3.5 h-3.5 shrink-0" />
                        <span>Foundational: Unlocks {item.chain_impact_count} advanced course{item.chain_impact_count > 1 ? 's' : ''}</span>
                      </div>
                    )}
                  </Card>
                ))}
              </div>
            )}
          </div>

          {/* Section: Recommended Later */}
          <div className="space-y-3 pt-3">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-warning flex items-center space-x-1.5">
              <Clock className="w-4 h-4" />
              <span>Recommended Later ({recLater.length}) — Pending Prerequisites or Subsequent Semesters</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
              {recLater.slice(0, 10).map((item) => (
                <Card
                  key={item.course.course_code}
                  className="space-y-3 shadow-xs hover:border-border"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-mono font-bold text-text-secondary">
                          {item.course.course_code}
                        </span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-surface-elevated text-text-secondary border border-border">
                          {item.course.credits} cr · Y{item.course.year} S{item.course.semester}
                        </span>
                      </div>
                      <h3 className="text-xs font-semibold text-text-primary mt-1">
                        {item.course.course_name}
                      </h3>
                      <p className="text-[11px] text-text-muted mt-0.5">{item.course.subject_area}</p>
                    </div>

                    <div className="text-right shrink-0">
                      <span className="text-[10px] uppercase font-semibold text-text-muted block">
                        Synergy
                      </span>
                      <span className="text-base font-black text-text-secondary">
                        {item.synergy_score}%
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-text-muted bg-bg-secondary rounded-lg p-2.5 border border-border-subtle leading-relaxed">
                    {item.reason}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Core Courses */}
      {activeTab === 'cores' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {core_courses.map((item) => (
              <Card
                key={item.course.course_code}
                padding="sm"
                className="space-y-2"
              >
                <div className="flex justify-between items-start gap-2">
                  <div>
                    <span className="text-xs font-mono font-semibold text-primary">
                      {item.course.course_code}
                    </span>
                    <h3 className="text-xs font-semibold text-text-primary mt-0.5">
                      {item.course.course_name}
                    </h3>
                  </div>
                  <Badge
                    variant={item.category === 'Recommended Now' ? 'success' : 'neutral'}
                    size="sm"
                  >
                    {item.category}
                  </Badge>
                </div>
                <p className="text-[11px] text-text-secondary leading-relaxed">{item.reason}</p>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Roadmap */}
      {activeTab === 'roadmap' && (
        <div className="space-y-6">
          {Object.entries(roadmap).map(([year, sems]) => (
            <Card key={year} className="space-y-4">
              <h3 className="text-sm font-bold text-text-primary border-b border-border-subtle pb-2">
                {year}
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {Object.entries(sems).map(([sem, coursesList]) => (
                  <div key={sem} className="space-y-2">
                    <span className="text-xs font-semibold text-primary block">
                      {sem} ({coursesList.length} courses)
                    </span>
                    <div className="space-y-1.5">
                      {coursesList.map((c) => (
                        <div
                          key={c.course_code}
                          className="bg-bg-secondary border border-border-subtle rounded-lg p-2.5 flex justify-between items-center text-xs"
                        >
                          <div>
                            <strong className="text-text-primary font-mono">{c.course_code}</strong>
                            <span className="text-text-secondary ml-2">{c.course_name}</span>
                          </div>
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-surface border border-border text-text-muted shrink-0">
                            {c.credits} cr
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-border flex items-center justify-between">
        <Button
          variant="secondary"
          size="md"
          icon={ArrowLeft}
          onClick={onPrev}
        >
          Back to Recommendations
        </Button>

        <Button
          variant="primary"
          size="lg"
          icon={ArrowRight}
          iconPosition="right"
          onClick={onNext}
        >
          View Graduation Audit
        </Button>
      </div>
    </div>
  );
}
