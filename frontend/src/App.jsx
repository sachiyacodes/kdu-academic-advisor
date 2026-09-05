import React, { useEffect } from 'react';
import Navbar from './components/Navbar';
import StepProfile from './components/StepProfile';
import StepCourseHistory from './components/StepCourseHistory';
import StepInterests from './components/StepInterests';
import StepRecommendations from './components/StepRecommendations';
import StepElectives from './components/StepElectives';
import StepGraduation from './components/StepGraduation';
import { useAdvisorState } from './useAdvisorState';
import { AlertCircle } from 'lucide-react';

export default function App() {
  const {
    currentStep, setCurrentStep, backendOnline, loading, error,
    degrees, catalogCourses, catalogInterests, specializations, demoProfiles,
    profile, setProfile, courses, setCourses, interests, setInterests,
    targetSpec, setTargetSpec, gpaData, recData, advisorData, auditData,
    runRecommendations, runElectivesAdvisor, runGraduationAudit,
    loadDemo, autofillPriorCourses, resetAll, completedSteps,
  } = useAdvisorState();

  useEffect(() => {
    if (currentStep === 4) runRecommendations();
    else if (currentStep === 5) runElectivesAdvisor();
    else if (currentStep === 6) runGraduationAudit();
  }, [currentStep, runRecommendations, runElectivesAdvisor, runGraduationAudit]);

  const handleTargetSpecChange = (newSpec) => {
    setTargetSpec(newSpec);
    runElectivesAdvisor(newSpec);
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'var(--color-bg-primary)',
      color: 'var(--color-text-primary)',
      display: 'flex',
      flexDirection: 'column',
      fontFamily: 'var(--font-sans)',
    }}>
      <Navbar
        currentStep={currentStep}
        setCurrentStep={setCurrentStep}
        completedSteps={completedSteps}
        demoProfiles={demoProfiles}
        onLoadDemo={loadDemo}
        onReset={resetAll}
        backendOnline={backendOnline}
      />

      <main style={{ flex: 1, padding: '0 24px 48px' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto' }}>

          {/* Error banner */}
          {error && (
            <div style={{
              display: 'flex', alignItems: 'flex-start', gap: '10px',
              padding: '12px 14px', margin: '16px 0',
              background: 'var(--color-danger-subtle)',
              border: '1px solid var(--color-danger-border)',
              borderRadius: '8px', fontSize: '12px',
            }}>
              <AlertCircle style={{ width: '14px', height: '14px', color: 'var(--color-danger)', flexShrink: 0, marginTop: '1px' }} />
              <div>
                <strong style={{ color: 'var(--color-danger)', fontWeight: 600 }}>Service notice: </strong>
                <span style={{ color: 'var(--color-text-secondary)' }}>{error}</span>
              </div>
            </div>
          )}

          {currentStep === 1 && (
            <StepProfile
              profile={profile} setProfile={setProfile}
              degrees={degrees} demoProfiles={demoProfiles}
              onLoadDemo={loadDemo} onNext={() => setCurrentStep(2)}
            />
          )}
          {currentStep === 2 && (
            <StepCourseHistory
              profile={profile} courses={courses} setCourses={setCourses}
              catalogCourses={catalogCourses} gpaData={gpaData}
              onAutofillPriorCourses={autofillPriorCourses}
              onPrev={() => setCurrentStep(1)} onNext={() => setCurrentStep(3)}
            />
          )}
          {currentStep === 3 && (
            <StepInterests
              interests={interests} setInterests={setInterests}
              catalogInterests={catalogInterests}
              onPrev={() => setCurrentStep(2)} onNext={() => setCurrentStep(4)}
            />
          )}
          {currentStep === 4 && (
            <StepRecommendations
              recData={recData} loading={loading}
              onPrev={() => setCurrentStep(3)} onNext={() => setCurrentStep(5)}
            />
          )}
          {currentStep === 5 && (
            <StepElectives
              advisorData={advisorData} loading={loading}
              targetSpec={targetSpec} setTargetSpec={handleTargetSpecChange}
              specializations={specializations}
              onPrev={() => setCurrentStep(4)} onNext={() => setCurrentStep(6)}
            />
          )}
          {currentStep === 6 && (
            <StepGraduation
              auditData={auditData} recData={recData} loading={loading}
              onPrev={() => setCurrentStep(5)} onReset={resetAll}
            />
          )}
        </div>
      </main>

      <footer style={{
        borderTop: '1px solid var(--color-border-subtle)',
        background: 'var(--color-bg-secondary)',
        padding: '16px 24px',
      }}>
        <div style={{
          maxWidth: '1280px', margin: '0 auto',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          fontSize: '11px', color: 'var(--color-text-muted)',
          flexWrap: 'wrap', gap: '4px',
        }}>
          <span>KDU Academic Advisor · Faculty of Computing</span>
          <span>IT3182 Essentials of AI · Group 22</span>
        </div>
      </footer>
    </div>
  );
}
