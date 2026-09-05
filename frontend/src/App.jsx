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
    currentStep,
    setCurrentStep,
    backendOnline,
    loading,
    error,
    degrees,
    catalogCourses,
    catalogInterests,
    specializations,
    demoProfiles,
    profile,
    setProfile,
    courses,
    setCourses,
    interests,
    setInterests,
    targetSpec,
    setTargetSpec,
    gpaData,
    recData,
    advisorData,
    auditData,
    runRecommendations,
    runElectivesAdvisor,
    runGraduationAudit,
    loadDemo,
    resetAll,
    completedSteps,
  } = useAdvisorState();

  // Trigger recalculations when switching to steps requiring backend pipeline results
  useEffect(() => {
    if (currentStep === 4) {
      runRecommendations();
    } else if (currentStep === 5) {
      runElectivesAdvisor();
    } else if (currentStep === 6) {
      runGraduationAudit();
    }
  }, [currentStep, runRecommendations, runElectivesAdvisor, runGraduationAudit]);

  // When targetSpec changes in step 5, re-fetch electives
  const handleTargetSpecChange = (newSpec) => {
    setTargetSpec(newSpec);
    runElectivesAdvisor(newSpec);
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Global Navbar */}
      <Navbar
        currentStep={currentStep}
        setCurrentStep={setCurrentStep}
        completedSteps={completedSteps}
        demoProfiles={demoProfiles}
        onLoadDemo={loadDemo}
        onReset={resetAll}
        backendOnline={backendOnline}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
            <div className="flex-1">
              <strong className="block font-semibold">Service Notice:</strong>
              <span>{error}</span>
            </div>
          </div>
        )}

        {currentStep === 1 && (
          <StepProfile
            profile={profile}
            setProfile={setProfile}
            degrees={degrees}
            demoProfiles={demoProfiles}
            onLoadDemo={loadDemo}
            onNext={() => setCurrentStep(2)}
          />
        )}

        {currentStep === 2 && (
          <StepCourseHistory
            profile={profile}
            courses={courses}
            setCourses={setCourses}
            catalogCourses={catalogCourses}
            gpaData={gpaData}
            onPrev={() => setCurrentStep(1)}
            onNext={() => setCurrentStep(3)}
          />
        )}

        {currentStep === 3 && (
          <StepInterests
            interests={interests}
            setInterests={setInterests}
            catalogInterests={catalogInterests}
            onPrev={() => setCurrentStep(2)}
            onNext={() => setCurrentStep(4)}
          />
        )}

        {currentStep === 4 && (
          <StepRecommendations
            recData={recData}
            loading={loading}
            onPrev={() => setCurrentStep(3)}
            onNext={() => setCurrentStep(5)}
          />
        )}

        {currentStep === 5 && (
          <StepElectives
            advisorData={advisorData}
            loading={loading}
            targetSpec={targetSpec}
            setTargetSpec={handleTargetSpecChange}
            specializations={specializations}
            onPrev={() => setCurrentStep(4)}
            onNext={() => setCurrentStep(6)}
          />
        )}

        {currentStep === 6 && (
          <StepGraduation
            auditData={auditData}
            recData={recData}
            loading={loading}
            onPrev={() => setCurrentStep(5)}
            onReset={resetAll}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            AI-Based IT Specialization & Course Recommendation System · KDU Faculty of Computing
          </span>
          <span>
            IT3182 Essentials of AI · Group 22 · Academic Prototype
          </span>
        </div>
      </footer>
    </div>
  );
}
