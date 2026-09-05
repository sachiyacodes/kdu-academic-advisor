/**
 * API client for the FastAPI backend.
 * Uses relative URL '/api' so it works seamlessly on both:
 * - Local development (Vite dev proxy -> http://127.0.0.1:8000)
 * - Vercel production serverless function (/api/index.py)
 */

const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to reach backend API');
  return res.json();
}

export async function fetchDegrees() {
  const res = await fetch(`${API_BASE}/catalog/degrees`);
  if (!res.ok) throw new Error('Failed to load degrees');
  return res.json();
}

export async function fetchCourses(degree = null) {
  const url = degree
    ? `${API_BASE}/catalog/courses?degree=${encodeURIComponent(degree)}`
    : `${API_BASE}/catalog/courses`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to load courses');
  return res.json();
}

export async function fetchInterests() {
  const res = await fetch(`${API_BASE}/catalog/interests`);
  if (!res.ok) throw new Error('Failed to load interests');
  return res.json();
}

export async function fetchSpecializations() {
  const res = await fetch(`${API_BASE}/catalog/specializations`);
  if (!res.ok) throw new Error('Failed to load specializations');
  return res.json();
}

export async function fetchDemoProfiles() {
  const res = await fetch(`${API_BASE}/catalog/demo-profiles`);
  if (!res.ok) throw new Error('Failed to load demo profiles');
  return res.json();
}

export async function calculateGpa(courses) {
  const res = await fetch(`${API_BASE}/gpa/calculate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(courses),
  });
  if (!res.ok) throw new Error('Failed to calculate GPA');
  return res.json();
}

export async function getRecommendations(payload) {
  const res = await fetch(`${API_BASE}/recommendations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to generate recommendations');
  return res.json();
}

export async function getElectivesAdvisor(payload) {
  const res = await fetch(`${API_BASE}/electives/advisor`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to load elective guidance');
  return res.json();
}

export async function getGraduationAudit(payload) {
  const res = await fetch(`${API_BASE}/audit/graduation`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to run graduation audit');
  return res.json();
}
