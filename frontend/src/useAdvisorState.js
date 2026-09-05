import { useState, useEffect, useCallback } from 'react';
import {
  fetchHealth,
  fetchDegrees,
  fetchCourses,
  fetchInterests,
  fetchSpecializations,
  fetchDemoProfiles,
  calculateGpa,
  getRecommendations,
  getElectivesAdvisor,
  getGraduationAudit,
} from './api';

const STORAGE_KEY = 'kdu_advisor_state_v1';

export function useAdvisorState() {
  const [currentStep, setCurrentStep] = useState(1);
  const [backendOnline, setBackendOnline] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Catalogs
  const [degrees, setDegrees] = useState([]);
  const [catalogCourses, setCatalogCourses] = useState([]);
  const [catalogInterests, setCatalogInterests] = useState([]);
  const [specializations, setSpecializations] = useState([]);
  const [demoProfiles, setDemoProfiles] = useState({});

  // Student Profile State
  const [profile, setProfile] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed.profile) return parsed.profile;
      } catch (e) {}
    }
    return {
      degree: 'Information Technology',
      year: 2,
      semester: 2,
    };
  });

  // Student Courses
  const [courses, setCourses] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed.courses) return parsed.courses;
      } catch (e) {}
    }
    return [];
  });

  // Student Interests: { [area]: intensity }
  const [interests, setInterests] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        if (parsed.interests) return parsed.interests;
      } catch (e) {}
    }
    return {};
  });

  // Target specialization for elective synergy
  const [targetSpec, setTargetSpec] = useState('Data Science');

  // Computed Outputs
  const [gpaData, setGpaData] = useState(null);
  const [recData, setRecData] = useState(null);
  const [advisorData, setAdvisorData] = useState(null);
  const [auditData, setAuditData] = useState(null);

  // Sync to LocalStorage
  useEffect(() => {
    const payload = {
      profile,
      courses,
      interests,
      targetSpec,
      currentStep,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  }, [profile, courses, interests, targetSpec, currentStep]);

  // Initial Load Catalogs & Health
  useEffect(() => {
    async function init() {
      try {
        setLoading(true);
        const health = await fetchHealth();
        setBackendOnline(health.status === 'healthy');

        const [degs, crs, ints, specs, demos] = await Promise.all([
          fetchDegrees(),
          fetchCourses(),
          fetchInterests(),
          fetchSpecializations(),
          fetchDemoProfiles(),
        ]);

        setDegrees(degs.degrees || []);
        setCatalogCourses(crs.courses || []);
        setCatalogInterests(ints.interests || []);
        setSpecializations(specs.specializations || []);
        setDemoProfiles(demos.profiles || {});

        // If courses already present in storage, calculate GPA
        if (courses.length > 0) {
          calculateGpa(courses).then(setGpaData).catch(console.error);
        }
      } catch (err) {
        console.error('Initialization error:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    init();
  }, []);

  // Update GPA on courses change
  useEffect(() => {
    if (courses.length > 0) {
      calculateGpa(courses)
        .then(setGpaData)
        .catch((e) => console.error('GPA Calc error:', e));
    } else {
      setGpaData(null);
    }
  }, [courses]);

  // Generate Recommendations Trigger
  const runRecommendations = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getRecommendations({
        degree: profile.degree,
        year: profile.year,
        semester: profile.semester,
        courses,
        interests,
      });
      setRecData(res);
      if (res.recommendations && res.recommendations.length > 0) {
        setTargetSpec(res.recommendations[0].specialization_name);
      }
    } catch (err) {
      console.error('Recommendation generation error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [profile, courses, interests]);

  // Generate Electives Advisor Trigger
  const runElectivesAdvisor = useCallback(async (specOverride = null) => {
    try {
      setLoading(true);
      setError(null);
      const res = await getElectivesAdvisor({
        degree: profile.degree,
        year: profile.year,
        semester: profile.semester,
        courses,
        target_specialization: specOverride || targetSpec,
      });
      setAdvisorData(res);
    } catch (err) {
      console.error('Advisor error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [profile, courses, targetSpec]);

  // Generate Graduation Audit Trigger
  const runGraduationAudit = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getGraduationAudit({
        degree: profile.degree,
        courses,
      });
      setAuditData(res);
    } catch (err) {
      console.error('Audit error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [profile, courses]);

  // Load Demo Archetype
  const loadDemo = useCallback(
    (profileKey) => {
      if (!demoProfiles || !demoProfiles[profileKey]) return;
      const demo = demoProfiles[profileKey];
      setProfile({
        degree: demo.degree,
        year: demo.year,
        semester: demo.semester,
      });
      setCourses(demo.courses || []);
      setInterests(demo.interests || {});
      setCurrentStep(4); // Jump directly to recommendations to see results
    },
    [demoProfiles]
  );

  // Reset All Data
  const resetAll = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setProfile({
      degree: 'Information Technology',
      year: 2,
      semester: 2,
    });
    setCourses([]);
    setInterests({});
    setGpaData(null);
    setRecData(null);
    setAdvisorData(null);
    setAuditData(null);
    setCurrentStep(1);
  }, []);

  // Compute completed steps
  const completedSteps = [];
  if (profile.degree) completedSteps.push(1);
  if (courses.length > 0) completedSteps.push(2);
  if (Object.keys(interests).length > 0) completedSteps.push(3);
  if (recData) completedSteps.push(4);
  if (advisorData) completedSteps.push(5);
  if (auditData) completedSteps.push(6);

  return {
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
  };
}
