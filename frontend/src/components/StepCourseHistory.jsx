import React, { useState, useMemo } from 'react';
import {
  BookOpen,
  Plus,
  Trash2,
  Sparkles,
  ArrowRight,
  ArrowLeft,
  X,
} from 'lucide-react';
import { Card, Button, Badge, IconButton } from './ui';

function getGradeInfo(mark) {
  const numMark = parseFloat(mark) || 0;
  if (numMark >= 85) return { grade: 'A+', gp: 4.0, variant: 'success' };
  if (numMark >= 75) return { grade: 'A', gp: 4.0, variant: 'success' };
  if (numMark >= 70) return { grade: 'A-', gp: 3.7, variant: 'success' };
  if (numMark >= 65) return { grade: 'B+', gp: 3.3, variant: 'primary' };
  if (numMark >= 60) return { grade: 'B', gp: 3.0, variant: 'primary' };
  if (numMark >= 55) return { grade: 'B-', gp: 2.7, variant: 'primary' };
  if (numMark >= 50) return { grade: 'C+', gp: 2.3, variant: 'warning' };
  if (numMark >= 45) return { grade: 'C', gp: 2.0, variant: 'warning' };
  if (numMark >= 40) return { grade: 'C-', gp: 1.7, variant: 'warning' };
  if (numMark >= 35) return { grade: 'D+', gp: 1.3, variant: 'danger' };
  if (numMark >= 30) return { grade: 'D', gp: 1.0, variant: 'danger' };
  return { grade: 'E', gp: 0.0, variant: 'danger' };
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

  // Custom Course Modal State
  const [isCustomModalOpen, setIsCustomModalOpen] = useState(false);
  const [customCourse, setCustomCourse] = useState({
    code: '',
    name: '',
    credits: 3,
    subjectArea: 'Programming & Software Development',
    courseType: 'Core',
    mark: 75,
  });

  // Filter available catalog courses for current degree
  const availableCatalogCourses = useMemo(() => {
    let list = catalogCourses;
    if (profile.degree !== 'Custom / Other University Degree') {
      list = list.filter((c) => c.degree === profile.degree);
    }
    return list;
  }, [catalogCourses, profile.degree]);

  // Already added course codes
  const addedCodes = useMemo(
    () => new Set(courses.map((c) => c.course_code)),
    [courses]
  );

  const handleAddCourse = (e) => {
    e.preventDefault();
    if (!selectedCourseCode) return;
    const cat = catalogCourses.find((c) => c.course_code === selectedCourseCode);
    if (!cat) return;

    const gradeInfo = getGradeInfo(markInput);
    const newRecord = {
      course_id: cat.course_id,
      course_code: cat.course_code,
      course_name: cat.course_name,
      credits: cat.credits,
      subject_area: cat.subject_area,
      course_type: cat.course_type,
      mark: parseFloat(markInput),
      grade: gradeInfo.grade,
      grade_point: gradeInfo.gp,
      status: 'completed',
      year: cat.year,
      semester: cat.semester,
    };

    setCourses([...courses.filter((c) => c.course_code !== cat.course_code), newRecord]);
    setSelectedCourseCode('');
  };

  const handleAddCustomCourse = (e) => {
    e.preventDefault();
    if (!customCourse.code || !customCourse.name) return;

    const gradeInfo = getGradeInfo(customCourse.mark);
    const newRecord = {
      course_id: Date.now(),
      course_code: customCourse.code.toUpperCase().trim(),
      course_name: customCourse.name.trim(),
      credits: parseInt(customCourse.credits, 10),
      subject_area: customCourse.subjectArea,
      course_type: customCourse.courseType,
      mark: parseFloat(customCourse.mark),
      grade: gradeInfo.grade,
      grade_point: gradeInfo.gp,
      status: 'completed',
      year: profile.year,
      semester: profile.semester,
    };

    setCourses([...courses.filter((c) => c.course_code !== newRecord.course_code), newRecord]);
    setIsCustomModalOpen(false);
    setCustomCourse({
      code: '',
      name: '',
      credits: 3,
      subjectArea: 'Programming & Software Development',
      courseType: 'Core',
      mark: 75,
    });
  };

  const handleRemoveCourse = (code) => {
    setCourses(courses.filter((c) => c.course_code !== code));
  };

  const currentGrade = getGradeInfo(markInput);

  const priorSemestersText = useMemo(() => {
    const y = profile.year || 2;
    const s = profile.semester || 2;
    if (y === 1 && s === 1) return 'Year 1 Sem 1 is your initial semester (no prior completed semesters)';
    if (y === 1 && s === 2) return 'Year 1 Semester 1';
    if (y === 2 && s === 1) return 'Year 1 (Semester 1 & 2)';
    if (y === 2 && s === 2) return 'Year 1 (Sem 1 & 2) + Year 2 Sem 1';
    if (y === 3 && s === 1) return 'Year 1 & Year 2 (Semesters 1 through 4)';
    if (y === 3 && s === 2) return 'Year 1, Year 2, and Year 3 Sem 1';
    return `All semesters prior to Year ${y} Semester ${s}`;
  }, [profile.year, profile.semester]);

  return (
    <div className="space-y-6 md:space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-border pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-primary text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 2 of 6</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-text-primary tracking-tight">
            Completed Course History
          </h1>
          <p className="text-sm text-text-secondary mt-1">
            Enter marks for completed courses. The engine automatically computes GPA, stage credits, and subject proficiencies.
          </p>
        </div>

        {/* GPA & Credits Stats Card */}
        {gpaData && (
          <Card padding="sm" className="flex items-center space-x-5 px-5 shrink-0">
            <div className="text-right">
              <span className="text-[11px] uppercase tracking-wider text-text-secondary font-semibold block">
                Current GPA
              </span>
              <span className="text-2xl font-black text-primary">
                {gpaData.gpa.toFixed(2)}
              </span>
            </div>
            <div className="h-8 w-px bg-border" />
            <div>
              <span className="text-[11px] uppercase tracking-wider text-text-secondary font-semibold block">
                Credits Earned
              </span>
              <span className="text-lg font-bold text-text-primary">
                {gpaData.credits_earned} <span className="text-xs text-text-muted">/ 134</span>
              </span>
            </div>
          </Card>
        )}
      </div>

      {/* Stage Context & Quick Autofill Banner */}
      <Card padding="normal" className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-lg bg-teal-subtle border border-teal-border flex items-center justify-center text-teal shrink-0">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-semibold text-text-primary">
                Current Stage: Year {profile.year}, Semester {profile.semester}
              </span>
              <Badge variant="neutral" size="sm">
                {profile.degree}
              </Badge>
            </div>
            <p className="text-xs text-text-secondary mt-0.5 leading-relaxed">
              Completed semesters: <strong className="text-text-primary">{priorSemestersText}</strong>. Marks for current semester are pending since you are currently enrolled.
            </p>
          </div>
        </div>

        {onAutofillPriorCourses && (
          <div className="flex items-center space-x-2 w-full sm:w-auto shrink-0">
            <Button
              variant="primary"
              size="md"
              icon={Sparkles}
              onClick={() => onAutofillPriorCourses('student_a')}
              title="Auto-fill all completed prior courses with benchmark marks"
              className="flex-1 sm:flex-none"
            >
              Auto-fill Prior Semesters
            </Button>
            {courses.length > 0 && (
              <Button
                variant="secondary"
                size="md"
                onClick={() => setCourses([])}
                title="Clear all course records"
              >
                Clear
              </Button>
            )}
          </div>
        )}
      </Card>

      {/* Add Course Form Section */}
      <Card className="space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
          <h2 className="text-sm font-semibold text-text-primary flex items-center space-x-2">
            <Plus className="w-4 h-4 text-primary" />
            <span>Record Course Grade</span>
          </h2>
          <button
            type="button"
            onClick={() => setIsCustomModalOpen(true)}
            className="text-xs text-primary hover:text-primary-hover font-medium hover:underline flex items-center space-x-1 cursor-pointer"
          >
            <span>+ Add Custom Course</span>
          </button>
        </div>

        <form onSubmit={handleAddCourse} className="grid grid-cols-1 sm:grid-cols-12 gap-3 items-end">
          {/* Course Selector */}
          <div className="sm:col-span-6 space-y-1.5">
            <label htmlFor="course-catalog-select" className="block text-xs font-semibold text-text-secondary">
              Select Course from Curriculum
            </label>
            <select
              id="course-catalog-select"
              value={selectedCourseCode}
              onChange={(e) => setSelectedCourseCode(e.target.value)}
              className="w-full h-11 bg-bg-secondary border border-border rounded-lg px-3 py-2 text-xs text-text-primary focus-ring transition cursor-pointer"
            >
              <option value="">-- Choose Course from Catalog --</option>
              {availableCatalogCourses.map((c) => {
                const isAdded = addedCodes.has(c.course_code);
                return (
                  <option key={c.course_code} value={c.course_code} disabled={isAdded} className="bg-surface text-text-primary">
                    {c.course_code} - {c.course_name} ({c.credits} cr · {c.subject_area}) {isAdded ? '✓ Added' : ''}
                  </option>
                );
              })}
            </select>
          </div>

          {/* Mark Input */}
          <div className="sm:col-span-3 space-y-1.5">
            <div className="flex justify-between items-center text-xs">
              <label htmlFor="mark-input" className="font-semibold text-text-secondary">Mark (0 - 100%)</label>
              <Badge variant={currentGrade.variant} size="sm">
                {currentGrade.grade} ({currentGrade.gp.toFixed(1)})
              </Badge>
            </div>
            <input
              id="mark-input"
              type="number"
              min="0"
              max="100"
              step="0.5"
              value={markInput}
              onChange={(e) => setMarkInput(e.target.value)}
              className="w-full h-11 bg-bg-secondary border border-border rounded-lg px-3.5 py-2 text-xs text-text-primary focus-ring transition"
            />
          </div>

          {/* Submit Button */}
          <div className="sm:col-span-3">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              disabled={!selectedCourseCode}
              icon={Plus}
              className="w-full"
            >
              Add to Transcript
            </Button>
          </div>
        </form>
      </Card>

      {/* Added Courses Section: High-Density Table replacing floating card boxes */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-text-primary flex items-center space-x-2">
            <BookOpen className="w-4 h-4 text-primary" />
            <span>Enrolled & Completed Courses ({courses.length})</span>
          </h2>
          {courses.length > 0 && (
            <button
              type="button"
              onClick={() => setCourses([])}
              className="text-xs text-text-muted hover:text-danger font-medium transition cursor-pointer"
            >
              Clear all courses
            </button>
          )}
        </div>

        {courses.length === 0 ? (
          <Card className="p-12 text-center space-y-3 border-dashed bg-bg-secondary/40">
            <BookOpen className="w-8 h-8 text-text-muted mx-auto" />
            <p className="text-sm text-text-primary font-semibold">
              No courses recorded yet
            </p>
            <p className="text-xs text-text-secondary max-w-md mx-auto leading-relaxed">
              Select courses above or click <strong>Auto-fill Prior Semesters</strong> to populate standard marks up to Year {profile.year} Semester {profile.semester}.
            </p>
          </Card>
        ) : (
          <div className="border border-border rounded-xl overflow-hidden bg-surface shadow-xs">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="bg-bg-secondary border-b border-border text-text-secondary font-semibold uppercase tracking-wider text-[11px]">
                    <th className="py-3 px-4 w-28">Code</th>
                    <th className="py-3 px-4">Course Name & Subject Area</th>
                    <th className="py-3 px-3 w-24">Type</th>
                    <th className="py-3 px-3 w-20 text-center">Credits</th>
                    <th className="py-3 px-3 w-20 text-center">Mark</th>
                    <th className="py-3 px-3 w-28 text-center">Grade</th>
                    <th className="py-3 px-4 w-16 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle">
                  {courses.map((c) => {
                    const gradeInfo = getGradeInfo(c.mark);
                    return (
                      <tr
                        key={c.course_code}
                        className="hover:bg-surface-hover transition-colors group"
                      >
                        {/* Course Code */}
                        <td className="py-3 px-4 font-mono font-semibold text-primary">
                          {c.course_code}
                        </td>

                        {/* Name & Area */}
                        <td className="py-3 px-4">
                          <div className="font-medium text-text-primary">{c.course_name}</div>
                          <div className="text-[11px] text-text-muted mt-0.5">{c.subject_area}</div>
                        </td>

                        {/* Type */}
                        <td className="py-3 px-3">
                          <Badge
                            variant={c.course_type === 'Core' ? 'neutral' : 'info'}
                            size="sm"
                          >
                            {c.course_type || 'Core'}
                          </Badge>
                        </td>

                        {/* Credits */}
                        <td className="py-3 px-3 text-center text-text-secondary font-medium">
                          {c.credits} cr
                        </td>

                        {/* Mark */}
                        <td className="py-3 px-3 text-center font-semibold text-text-primary">
                          {c.mark}%
                        </td>

                        {/* Grade */}
                        <td className="py-3 px-3 text-center">
                          <Badge variant={gradeInfo.variant} size="sm">
                            {gradeInfo.grade} ({gradeInfo.gp.toFixed(1)})
                          </Badge>
                        </td>

                        {/* Actions */}
                        <td className="py-3 px-4 text-right">
                          <IconButton
                            icon={Trash2}
                            label={`Remove course ${c.course_code}`}
                            variant="destructive"
                            size="sm"
                            onClick={() => handleRemoveCourse(c.course_code)}
                          />
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

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-border flex items-center justify-between">
        <Button
          variant="secondary"
          size="md"
          icon={ArrowLeft}
          onClick={onPrev}
        >
          Back to Profile
        </Button>

        <Button
          variant="primary"
          size="lg"
          icon={ArrowRight}
          iconPosition="right"
          onClick={onNext}
        >
          Proceed to Career Interests
        </Button>
      </div>

      {/* Custom Course Modal */}
      {isCustomModalOpen && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card variant="elevated" className="max-w-lg w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border-subtle">
              <h3 className="text-base font-bold text-text-primary">Add Custom Course</h3>
              <IconButton
                icon={X}
                label="Close custom course modal"
                size="sm"
                onClick={() => setIsCustomModalOpen(false)}
              />
            </div>
            <p className="text-xs text-text-secondary leading-relaxed">
              Enter custom course details from any curriculum, university, or credit transfer.
            </p>

            <form onSubmit={handleAddCustomCourse} className="space-y-3.5 text-xs">
              <div>
                <label className="block text-text-secondary font-semibold mb-1">Course Code</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. CS3050"
                  value={customCourse.code}
                  onChange={(e) => setCustomCourse({ ...customCourse, code: e.target.value })}
                  className="w-full h-10 bg-bg-secondary border border-border rounded-lg px-3 text-text-primary focus-ring"
                />
              </div>

              <div>
                <label className="block text-text-secondary font-semibold mb-1">Course Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Distributed Cloud Architectures"
                  value={customCourse.name}
                  onChange={(e) => setCustomCourse({ ...customCourse, name: e.target.value })}
                  className="w-full h-10 bg-bg-secondary border border-border rounded-lg px-3 text-text-primary focus-ring"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-text-secondary font-semibold mb-1">Credits</label>
                  <input
                    type="number"
                    min="1"
                    max="6"
                    value={customCourse.credits}
                    onChange={(e) => setCustomCourse({ ...customCourse, credits: e.target.value })}
                    className="w-full h-10 bg-bg-secondary border border-border rounded-lg px-3 text-text-primary focus-ring"
                  />
                </div>
                <div>
                  <label className="block text-text-secondary font-semibold mb-1">Course Type</label>
                  <select
                    value={customCourse.courseType}
                    onChange={(e) => setCustomCourse({ ...customCourse, courseType: e.target.value })}
                    className="w-full h-10 bg-bg-secondary border border-border rounded-lg px-3 text-text-primary focus-ring cursor-pointer"
                  >
                    <option value="Core" className="bg-surface text-text-primary">Core</option>
                    <option value="Elective" className="bg-surface text-text-primary">Elective</option>
                    <option value="NGPA" className="bg-surface text-text-primary">NGPA</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-text-secondary font-semibold mb-1">Subject Taxonomy Area</label>
                <select
                  value={customCourse.subjectArea}
                  onChange={(e) => setCustomCourse({ ...customCourse, subjectArea: e.target.value })}
                  className="w-full h-10 bg-bg-secondary border border-border rounded-lg px-3 text-text-primary focus-ring cursor-pointer"
                >
                  <option value="Programming & Software Development" className="bg-surface text-text-primary">Programming & Software Development</option>
                  <option value="Mathematics & Statistics" className="bg-surface text-text-primary">Mathematics & Statistics</option>
                  <option value="Database Systems" className="bg-surface text-text-primary">Database Systems</option>
                  <option value="Data Science & Analytics" className="bg-surface text-text-primary">Data Science & Analytics</option>
                  <option value="Artificial Intelligence" className="bg-surface text-text-primary">Artificial Intelligence</option>
                  <option value="Computer Networks" className="bg-surface text-text-primary">Computer Networks</option>
                  <option value="Cyber Security" className="bg-surface text-text-primary">Cyber Security</option>
                  <option value="Systems & Architecture" className="bg-surface text-text-primary">Systems & Architecture</option>
                  <option value="Web & Mobile Development" className="bg-surface text-text-primary">Web & Mobile Development</option>
                  <option value="Theoretical Computer Science" className="bg-surface text-text-primary">Theoretical Computer Science</option>
                  <option value="IT Management & Professional Practice" className="bg-surface text-text-primary">IT Management & Professional Practice</option>
                </select>
              </div>

              <div>
                <label className="block text-text-secondary font-semibold mb-1">Mark Earned (0 - 100%)</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  step="0.5"
                  value={customCourse.mark}
                  onChange={(e) => setCustomCourse({ ...customCourse, mark: e.target.value })}
                  className="w-full h-10 bg-bg-secondary border border-border rounded-lg px-3 text-text-primary focus-ring"
                />
              </div>

              <div className="pt-4 border-t border-border-subtle flex justify-end space-x-3">
                <Button
                  type="button"
                  variant="secondary"
                  size="md"
                  onClick={() => setIsCustomModalOpen(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                >
                  Add Course
                </Button>
              </div>
            </form>
          </Card>
        </div>
      )}
    </div>
  );
}
