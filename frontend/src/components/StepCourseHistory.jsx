import React, { useState, useMemo } from 'react';
import {
  BookOpen, Plus, Trash2, Sparkles, ArrowRight, ArrowLeft, X,
} from 'lucide-react';
import { Button, Badge, IconButton } from './ui';

function getGradeInfo(mark) {
  const n = parseFloat(mark) || 0;
  if (n >= 85) return { grade: 'A+', gp: 4.0, variant: 'success' };
  if (n >= 75) return { grade: 'A',  gp: 4.0, variant: 'success' };
  if (n >= 70) return { grade: 'A-', gp: 3.7, variant: 'success' };
  if (n >= 65) return { grade: 'B+', gp: 3.3, variant: 'primary' };
  if (n >= 60) return { grade: 'B',  gp: 3.0, variant: 'primary' };
  if (n >= 55) return { grade: 'B-', gp: 2.7, variant: 'primary' };
  if (n >= 50) return { grade: 'C+', gp: 2.3, variant: 'warning' };
  if (n >= 45) return { grade: 'C',  gp: 2.0, variant: 'warning' };
  if (n >= 40) return { grade: 'C-', gp: 1.7, variant: 'warning' };
  if (n >= 35) return { grade: 'D+', gp: 1.3, variant: 'danger' };
  if (n >= 30) return { grade: 'D',  gp: 1.0, variant: 'danger' };
  return        { grade: 'E',  gp: 0.0, variant: 'danger' };
}

export default function StepCourseHistory({
  profile,
  courses,
  setCourses,
  catalogCourses,
  gpaData,
  onAutofillPriorCourses,
  onPrev,
  onNext,
}) {
  const [selectedCourseCode, setSelectedCourseCode] = useState('');
  const [markInput, setMarkInput] = useState(75);
  const [isCustomModalOpen, setIsCustomModalOpen] = useState(false);
  const [customCourse, setCustomCourse] = useState({
    code: '', name: '', credits: 3,
    subjectArea: 'Programming & Software Development',
    courseType: 'Core', mark: 75,
  });

  const availableCatalogCourses = useMemo(() => {
    if (profile.degree === 'Custom / Other University Degree') return catalogCourses;
    return catalogCourses.filter((c) => c.degree === profile.degree);
  }, [catalogCourses, profile.degree]);

  const addedCodes = useMemo(() => new Set(courses.map((c) => c.course_code)), [courses]);

  const handleAddCourse = (e) => {
    e.preventDefault();
    if (!selectedCourseCode) return;
    const cat = catalogCourses.find((c) => c.course_code === selectedCourseCode);
    if (!cat) return;
    const gi = getGradeInfo(markInput);
    setCourses([
      ...courses.filter((c) => c.course_code !== cat.course_code),
      {
        course_id: cat.course_id, course_code: cat.course_code, course_name: cat.course_name,
        credits: cat.credits, subject_area: cat.subject_area, course_type: cat.course_type,
        mark: parseFloat(markInput), grade: gi.grade, grade_point: gi.gp,
        status: 'completed', year: cat.year, semester: cat.semester,
      },
    ]);
    setSelectedCourseCode('');
  };

  const handleAddCustomCourse = (e) => {
    e.preventDefault();
    if (!customCourse.code || !customCourse.name) return;
    const gi = getGradeInfo(customCourse.mark);
    const rec = {
      course_id: Date.now(), course_code: customCourse.code.toUpperCase().trim(),
      course_name: customCourse.name.trim(), credits: parseInt(customCourse.credits, 10),
      subject_area: customCourse.subjectArea, course_type: customCourse.courseType,
      mark: parseFloat(customCourse.mark), grade: gi.grade, grade_point: gi.gp,
      status: 'completed', year: profile.year, semester: profile.semester,
    };
    setCourses([...courses.filter((c) => c.course_code !== rec.course_code), rec]);
    setIsCustomModalOpen(false);
    setCustomCourse({ code: '', name: '', credits: 3, subjectArea: 'Programming & Software Development', courseType: 'Core', mark: 75 });
  };

  const handleRemoveCourse = (code) => setCourses(courses.filter((c) => c.course_code !== code));
  const currentGrade = getGradeInfo(markInput);

  const priorSemestersText = useMemo(() => {
    const y = profile.year || 2, s = profile.semester || 2;
    if (y === 1 && s === 1) return 'This is your initial semester — no prior semesters.';
    if (y === 1 && s === 2) return 'Year 1, Semester 1';
    if (y === 2 && s === 1) return 'Year 1 (Sem 1 & 2)';
    if (y === 2 && s === 2) return 'Year 1 (Sem 1 & 2) + Year 2, Sem 1';
    if (y === 3 && s === 1) return 'Year 1 & 2 (Semesters 1–4)';
    if (y === 3 && s === 2) return 'Year 1, 2, and Year 3 Sem 1';
    return `All semesters before Year ${y} Semester ${s}`;
  }, [profile.year, profile.semester]);

  return (
    <div className="animate-fadeIn" style={{ maxWidth: '960px', margin: '0 auto' }}>

      {/* ── Header ───────────────────────────────────────────────── */}
      <div style={{
        padding: '32px 0 24px', borderBottom: '1px solid var(--color-border-subtle)',
        display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '24px',
      }}>
        <div>
          <h1 style={{ fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em', color: 'var(--color-text-primary)', margin: 0, lineHeight: 1.3 }}>
            Course History
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: '6px 0 0', lineHeight: 1.6 }}>
            Record marks for completed courses. GPA and subject proficiencies are computed automatically.
          </p>
        </div>

        {/* GPA stats */}
        {gpaData && (
          <div style={{
            display: 'flex', alignItems: 'center', gap: '20px',
            background: 'var(--color-surface)', border: '1px solid var(--color-border)',
            borderRadius: '10px', padding: '12px 18px', flexShrink: 0,
          }}>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '10px', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.05em', marginBottom: '2px' }}>GPA</div>
              <div style={{ fontSize: '22px', fontWeight: 800, color: 'var(--color-primary)', letterSpacing: '-0.02em', fontVariantNumeric: 'tabular-nums' }}>
                {gpaData.gpa.toFixed(2)}
              </div>
            </div>
            <div style={{ width: '1px', height: '32px', background: 'var(--color-border)' }} />
            <div>
              <div style={{ fontSize: '10px', fontWeight: 600, color: 'var(--color-text-muted)', letterSpacing: '0.05em', marginBottom: '2px' }}>CREDITS</div>
              <div style={{ fontSize: '16px', fontWeight: 700, color: 'var(--color-text-primary)', fontVariantNumeric: 'tabular-nums' }}>
                {gpaData.credits_earned}<span style={{ fontSize: '12px', color: 'var(--color-text-muted)', fontWeight: 400 }}> / 134</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Autofill banner ──────────────────────────────────────── */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        gap: '16px', padding: '14px 16px', margin: '20px 0',
        background: 'var(--color-teal-subtle)', border: '1px solid var(--color-teal-border)',
        borderRadius: '10px',
      }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
          <Sparkles style={{ width: '14px', height: '14px', color: 'var(--color-teal)', flexShrink: 0, marginTop: '2px' }} />
          <div>
            <div style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: '2px' }}>
              Year {profile.year}, Semester {profile.semester}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
              Completed semesters: <strong style={{ color: 'var(--color-text-primary)' }}>{priorSemestersText}</strong>
            </div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
          {onAutofillPriorCourses && (
            <Button variant="teal" size="sm" icon={Sparkles} onClick={() => onAutofillPriorCourses('student_a')}>
              Auto-fill prior semesters
            </Button>
          )}
          {courses.length > 0 && (
            <Button variant="secondary" size="sm" onClick={() => setCourses([])}>Clear all</Button>
          )}
        </div>
      </div>

      {/* ── Add course form ──────────────────────────────────────── */}
      <div style={{
        background: 'var(--color-surface)', border: '1px solid var(--color-border)',
        borderRadius: '10px', padding: '16px', marginBottom: '20px',
      }}>
        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          marginBottom: '14px',
        }}>
          <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Plus style={{ width: '13px', height: '13px', color: 'var(--color-text-muted)' }} />
            Record a grade
          </span>
          <button
            type="button"
            onClick={() => setIsCustomModalOpen(true)}
            style={{
              fontSize: '12px', color: 'var(--color-primary)', fontWeight: 500,
              background: 'none', border: 'none', cursor: 'pointer', padding: 0,
            }}
            className="focus-ring"
          >
            + Add custom course
          </button>
        </div>

        <form onSubmit={handleAddCourse}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 140px 140px', gap: '10px', alignItems: 'flex-end' }} className="add-course-grid">
            {/* Course selector */}
            <div>
              <label htmlFor="course-catalog-select" style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '6px' }}>
                Course
              </label>
              <select
                id="course-catalog-select"
                value={selectedCourseCode}
                onChange={(e) => setSelectedCourseCode(e.target.value)}
                style={{
                  width: '100%', height: '38px',
                  background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)',
                  borderRadius: '8px', padding: '0 10px', fontSize: '12px',
                  color: 'var(--color-text-primary)', cursor: 'pointer', outline: 'none',
                }}
                className="focus-ring"
              >
                <option value="">Select from curriculum...</option>
                {availableCatalogCourses.map((c) => {
                  const added = addedCodes.has(c.course_code);
                  return (
                    <option key={c.course_code} value={c.course_code} disabled={added} style={{ background: 'var(--color-surface)' }}>
                      {c.course_code} — {c.course_name} ({c.credits} cr){added ? '  ✓' : ''}
                    </option>
                  );
                })}
              </select>
            </div>

            {/* Mark input */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <label htmlFor="mark-input" style={{ fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)' }}>Mark %</label>
                <Badge variant={currentGrade.variant} size="sm">{currentGrade.grade}</Badge>
              </div>
              <input
                id="mark-input"
                type="number" min="0" max="100" step="0.5"
                value={markInput}
                onChange={(e) => setMarkInput(e.target.value)}
                style={{
                  width: '100%', height: '38px',
                  background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)',
                  borderRadius: '8px', padding: '0 10px', fontSize: '13px',
                  color: 'var(--color-text-primary)', outline: 'none',
                  fontVariantNumeric: 'tabular-nums',
                }}
                className="focus-ring"
              />
            </div>

            {/* Submit */}
            <div>
              <div style={{ height: '23px' }} /> {/* spacer aligns with inputs that have labels */}
              <Button type="submit" variant="primary" size="md" disabled={!selectedCourseCode} icon={Plus} className="w-full">
                Add
              </Button>
            </div>
          </div>
        </form>
      </div>

      {/* ── Transcript table ─────────────────────────────────────── */}
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <BookOpen style={{ width: '13px', height: '13px', color: 'var(--color-text-muted)' }} />
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--color-text-primary)' }}>
              Transcript
            </span>
            {courses.length > 0 && (
              <span style={{
                fontSize: '11px', color: 'var(--color-text-muted)',
                background: 'var(--color-surface)', border: '1px solid var(--color-border)',
                borderRadius: '20px', padding: '1px 8px',
              }}>
                {courses.length} courses
              </span>
            )}
          </div>
        </div>

        {courses.length === 0 ? (
          <div style={{
            border: '1px dashed var(--color-border)', borderRadius: '10px',
            padding: '48px 24px', textAlign: 'center',
            background: 'var(--color-bg-secondary)',
          }}>
            <BookOpen style={{ width: '24px', height: '24px', color: 'var(--color-text-disabled)', margin: '0 auto 12px' }} />
            <p style={{ fontSize: '13px', fontWeight: 600, color: 'var(--color-text-primary)', margin: '0 0 6px' }}>
              No courses recorded
            </p>
            <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', margin: 0, lineHeight: 1.5 }}>
              Select a course above or click <strong style={{ color: 'var(--color-teal)' }}>Auto-fill prior semesters</strong> to populate your transcript.
            </p>
          </div>
        ) : (
          <div style={{
            border: '1px solid var(--color-border)', borderRadius: '10px', overflow: 'hidden',
          }}>
            <div style={{ overflowX: 'auto' }}>
              <table className="academic-table" style={{ minWidth: '640px' }}>
                <thead>
                  <tr>
                    <th>Code</th>
                    <th>Course</th>
                    <th>Type</th>
                    <th style={{ textAlign: 'center' }}>Cr</th>
                    <th style={{ textAlign: 'center' }}>Mark</th>
                    <th style={{ textAlign: 'center' }}>Grade</th>
                    <th style={{ textAlign: 'right' }}></th>
                  </tr>
                </thead>
                <tbody>
                  {courses.map((c) => {
                    const gi = getGradeInfo(c.mark);
                    return (
                      <tr key={c.course_code}>
                        <td>
                          <span className="course-code">{c.course_code}</span>
                        </td>
                        <td>
                          <div style={{ fontWeight: 500, fontSize: '12px', color: 'var(--color-text-primary)' }}>{c.course_name}</div>
                          <div style={{ fontSize: '11px', color: 'var(--color-text-muted)', marginTop: '1px' }}>{c.subject_area}</div>
                        </td>
                        <td>
                          <Badge variant={c.course_type === 'Core' ? 'neutral' : 'info'} size="sm">
                            {c.course_type || 'Core'}
                          </Badge>
                        </td>
                        <td style={{ textAlign: 'center', color: 'var(--color-text-secondary)', fontSize: '12px', fontVariantNumeric: 'tabular-nums' }}>
                          {c.credits}
                        </td>
                        <td style={{ textAlign: 'center', fontWeight: 600, fontSize: '12px', fontVariantNumeric: 'tabular-nums', color: 'var(--color-text-primary)' }}>
                          {c.mark}%
                        </td>
                        <td style={{ textAlign: 'center' }}>
                          <Badge variant={gi.variant} size="sm">
                            {gi.grade} <span style={{ opacity: 0.7 }}>({gi.gp.toFixed(1)})</span>
                          </Badge>
                        </td>
                        <td style={{ textAlign: 'right' }}>
                          <IconButton icon={Trash2} label={`Remove ${c.course_code}`} variant="destructive" size="sm" onClick={() => handleRemoveCourse(c.course_code)} />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* ── Navigation ───────────────────────────────────────────── */}
      <div style={{ paddingTop: '20px', borderTop: '1px solid var(--color-border-subtle)', display: 'flex', justifyContent: 'space-between' }}>
        <Button variant="secondary" size="md" icon={ArrowLeft} onClick={onPrev}>Profile</Button>
        <Button variant="primary" size="lg" icon={ArrowRight} iconPosition="right" onClick={onNext}>Career Interests</Button>
      </div>

      {/* ── Custom course modal ──────────────────────────────────── */}
      {isCustomModalOpen && (
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)',
          backdropFilter: 'blur(4px)', zIndex: 100,
          display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px',
        }}>
          <div style={{
            background: 'var(--color-surface-elevated)', border: '1px solid var(--color-border)',
            borderRadius: '12px', padding: '24px', width: '100%', maxWidth: '480px',
            boxShadow: '0 24px 48px rgba(0,0,0,0.4)',
          }} className="animate-fadeUp">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px', paddingBottom: '14px', borderBottom: '1px solid var(--color-border-subtle)' }}>
              <h3 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--color-text-primary)', margin: 0 }}>Add custom course</h3>
              <IconButton icon={X} label="Close" size="sm" onClick={() => setIsCustomModalOpen(false)} />
            </div>

            <form onSubmit={handleAddCustomCourse} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {[
                { label: 'Course code', field: 'code', type: 'text', placeholder: 'e.g. CS3050', required: true },
                { label: 'Course title', field: 'name', type: 'text', placeholder: 'e.g. Distributed Cloud Architectures', required: true },
              ].map(({ label, field, type, placeholder, required }) => (
                <div key={field}>
                  <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '6px' }}>{label}</label>
                  <input
                    type={type} required={required} placeholder={placeholder}
                    value={customCourse[field]}
                    onChange={(e) => setCustomCourse({ ...customCourse, [field]: e.target.value })}
                    style={{ width: '100%', height: '38px', background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '0 10px', fontSize: '13px', color: 'var(--color-text-primary)', outline: 'none' }}
                    className="focus-ring"
                  />
                </div>
              ))}

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '6px' }}>Credits</label>
                  <input type="number" min="1" max="6" value={customCourse.credits}
                    onChange={(e) => setCustomCourse({ ...customCourse, credits: e.target.value })}
                    style={{ width: '100%', height: '38px', background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '0 10px', fontSize: '13px', color: 'var(--color-text-primary)', outline: 'none' }}
                    className="focus-ring"
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '6px' }}>Type</label>
                  <select value={customCourse.courseType} onChange={(e) => setCustomCourse({ ...customCourse, courseType: e.target.value })}
                    style={{ width: '100%', height: '38px', background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '0 10px', fontSize: '12px', color: 'var(--color-text-primary)', outline: 'none', cursor: 'pointer' }}
                    className="focus-ring">
                    <option value="Core">Core</option>
                    <option value="Elective">Elective</option>
                    <option value="NGPA">NGPA</option>
                  </select>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '6px' }}>Subject area</label>
                <select value={customCourse.subjectArea} onChange={(e) => setCustomCourse({ ...customCourse, subjectArea: e.target.value })}
                  style={{ width: '100%', height: '38px', background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '0 10px', fontSize: '12px', color: 'var(--color-text-primary)', outline: 'none', cursor: 'pointer' }}
                  className="focus-ring">
                  {['Programming & Software Development','Mathematics & Statistics','Database Systems','Data Science & Analytics','Artificial Intelligence','Computer Networks','Cyber Security','Systems & Architecture','Web & Mobile Development','Theoretical Computer Science','IT Management & Professional Practice'].map(a => (
                    <option key={a} value={a} style={{ background: 'var(--color-surface)' }}>{a}</option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '11px', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: '6px' }}>Mark (0–100%)</label>
                <input type="number" min="0" max="100" step="0.5" value={customCourse.mark}
                  onChange={(e) => setCustomCourse({ ...customCourse, mark: e.target.value })}
                  style={{ width: '100%', height: '38px', background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '0 10px', fontSize: '13px', color: 'var(--color-text-primary)', outline: 'none' }}
                  className="focus-ring"
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', paddingTop: '8px', borderTop: '1px solid var(--color-border-subtle)' }}>
                <Button type="button" variant="secondary" size="md" onClick={() => setIsCustomModalOpen(false)}>Cancel</Button>
                <Button type="submit" variant="primary" size="md">Add course</Button>
              </div>
            </form>
          </div>
        </div>
      )}

      <style>{`
        @media (max-width: 640px) {
          .add-course-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  );
}
