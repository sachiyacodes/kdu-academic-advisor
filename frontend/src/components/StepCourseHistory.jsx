import React, { useState, useMemo } from 'react';
import {
  BookOpen,
  Plus,
  Trash2,
  Award,
  CheckCircle2,
  ArrowRight,
  ArrowLeft,
  Search,
  Filter,
  Layers,
  Sparkles,
} from 'lucide-react';

function getGradeInfo(mark) {
  if (mark >= 85) return { grade: 'A+', gp: 4.0, color: 'text-emerald-400 bg-emerald-950/40 border-emerald-800/50' };
  if (mark >= 75) return { grade: 'A', gp: 4.0, color: 'text-emerald-400 bg-emerald-950/40 border-emerald-800/50' };
  if (mark >= 70) return { grade: 'A-', gp: 3.7, color: 'text-emerald-300 bg-emerald-950/40 border-emerald-800/50' };
  if (mark >= 65) return { grade: 'B+', gp: 3.3, color: 'text-indigo-300 bg-indigo-950/40 border-indigo-800/50' };
  if (mark >= 60) return { grade: 'B', gp: 3.0, color: 'text-indigo-400 bg-indigo-950/40 border-indigo-800/50' };
  if (mark >= 55) return { grade: 'B-', gp: 2.7, color: 'text-indigo-400 bg-indigo-950/40 border-indigo-800/50' };
  if (mark >= 50) return { grade: 'C+', gp: 2.3, color: 'text-amber-300 bg-amber-950/40 border-amber-800/50' };
  if (mark >= 45) return { grade: 'C', gp: 2.0, color: 'text-amber-400 bg-amber-950/40 border-amber-800/50' };
  if (mark >= 40) return { grade: 'C-', gp: 1.7, color: 'text-amber-500 bg-amber-950/40 border-amber-800/50' };
  if (mark >= 35) return { grade: 'D+', gp: 1.3, color: 'text-rose-400 bg-rose-950/40 border-rose-800/50' };
  if (mark >= 30) return { grade: 'D', gp: 1.0, color: 'text-rose-400 bg-rose-950/40 border-rose-800/50' };
  return { grade: 'E', gp: 0.0, color: 'text-rose-500 bg-rose-950/40 border-rose-800/50' };
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
  const [searchTerm, setSearchTerm] = useState('');
  const [filterYear, setFilterYear] = useState('all');

  // Custom Course Form Modal State
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
    if (filterYear !== 'all') {
      list = list.filter((c) => c.year === parseInt(filterYear, 10));
    }
    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      list = list.filter(
        (c) =>
          c.course_code.toLowerCase().includes(q) ||
          c.course_name.toLowerCase().includes(q) ||
          c.subject_area.toLowerCase().includes(q)
      );
    }
    return list;
  }, [catalogCourses, profile.degree, filterYear, searchTerm]);

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
    if (y === 1 && s === 1) return 'Year 1 Sem 1 is your current initial semester (no prior completed semesters)';
    if (y === 1 && s === 2) return 'Year 1 Semester 1';
    if (y === 2 && s === 1) return 'Year 1 (Semester 1 & 2)';
    if (y === 2 && s === 2) return 'Year 1 (Sem 1 & 2) + Year 2 Sem 1';
    if (y === 3 && s === 1) return 'Year 1 & Year 2 (Semesters 1 through 4)';
    if (y === 3 && s === 2) return 'Year 1, Year 2, and Year 3 Sem 1';
    return `All semesters prior to Year ${y} Semester ${s}`;
  }, [profile.year, profile.semester]);

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 2 of 6</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Completed Course History
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Enter marks for completed courses. The system automatically computes GPA, stage standing, and subject area proficiencies.
          </p>
        </div>

        {/* GPA & Credits Stats Card */}
        {gpaData && (
          <div className="flex items-center space-x-4 bg-slate-900 border border-slate-800 rounded-2xl p-3.5 px-5 shadow-lg">
            <div className="text-right">
              <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold block">
                Current GPA
              </span>
              <span className="text-2xl font-black text-indigo-400">
                {gpaData.gpa.toFixed(2)}
              </span>
            </div>
            <div className="h-8 w-px bg-slate-800" />
            <div>
              <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold block">
                Credits Earned
              </span>
              <span className="text-lg font-bold text-slate-200">
                {gpaData.credits_earned} <span className="text-xs text-slate-500">/ 134</span>
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Stage Context & Quick Autofill Banner */}
      <div className="bg-gradient-to-r from-indigo-950/40 via-purple-950/30 to-slate-900 border border-indigo-800/40 rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-slate-200">
                Current Stage: Year {profile.year}, Semester {profile.semester}
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-900/60 text-indigo-300 border border-indigo-700/50">
                {profile.degree}
              </span>
            </div>
            <p className="text-[11px] text-slate-400 mt-0.5">
              Completed semesters: <strong className="text-slate-300">{priorSemestersText}</strong>. Marks for current semester are pending since you are currently studying it.
            </p>
          </div>
        </div>

        {onAutofillPriorCourses && (
          <div className="flex items-center space-x-2 w-full sm:w-auto">
            <button
              type="button"
              onClick={() => onAutofillPriorCourses('student_a')}
              className="flex-1 sm:flex-none flex items-center justify-center space-x-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 transition cursor-pointer"
              title="Auto-fill all completed prior courses with benchmark marks"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Auto-fill Prior Semesters</span>
            </button>
            {courses.length > 0 && (
              <button
                type="button"
                onClick={() => setCourses([])}
                className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-rose-950/50 hover:text-rose-300 hover:border-rose-800/50 border border-slate-700 text-slate-400 text-xs font-medium transition cursor-pointer"
                title="Clear all course records"
              >
                Clear
              </button>
            )}
          </div>
        )}
      </div>

      {/* Add Course Form Section */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
            <Plus className="w-4 h-4 text-indigo-400" />
            <span>Record Course Grade</span>
          </h2>
          <button
            type="button"
            onClick={() => setIsCustomModalOpen(true)}
            className="text-xs text-indigo-400 hover:text-indigo-300 font-medium hover:underline flex items-center space-x-1"
          >
            <span>+ Add Custom Course</span>
          </button>
        </div>

        <form onSubmit={handleAddCourse} className="grid grid-cols-1 sm:grid-cols-12 gap-4 items-end">
          {/* Course Selector */}
          <div className="sm:col-span-6 space-y-1.5">
            <label className="block text-xs font-medium text-slate-300">
              Select Course from Curriculum
            </label>
            <select
              value={selectedCourseCode}
              onChange={(e) => setSelectedCourseCode(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2.5 text-xs text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">-- Choose Course --</option>
              {availableCatalogCourses.map((c) => {
                const isAdded = addedCodes.has(c.course_code);
                return (
                  <option key={c.course_code} value={c.course_code} disabled={isAdded}>
                    {c.course_code} - {c.course_name} ({c.credits} cr · {c.subject_area}) {isAdded ? '✓ Already Added' : ''}
                  </option>
                );
              })}
            </select>
          </div>

          {/* Mark Input */}
          <div className="sm:col-span-3 space-y-1.5">
            <div className="flex justify-between items-center text-xs">
              <label className="font-medium text-slate-300">Mark (0 - 100%)</label>
              <span className={`px-2 py-0.5 rounded text-[11px] font-bold border ${currentGrade.color}`}>
                Grade: {currentGrade.grade} ({currentGrade.gp.toFixed(1)})
              </span>
            </div>
            <input
              type="number"
              min="0"
              max="100"
              step="0.5"
              value={markInput}
              onChange={(e) => setMarkInput(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          {/* Submit Button */}
          <div className="sm:col-span-3">
            <button
              type="submit"
              disabled={!selectedCourseCode}
              className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-semibold py-2.5 rounded-xl shadow-md shadow-indigo-600/20 transition flex items-center justify-center space-x-1.5"
            >
              <Plus className="w-4 h-4" />
              <span>Add to Transcript</span>
            </button>
          </div>
        </form>
      </div>

      {/* Added Courses Table / Cards */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-white flex items-center space-x-2">
            <BookOpen className="w-4 h-4 text-indigo-400" />
            <span>Enrolled & Completed Courses ({courses.length})</span>
          </h2>
          {courses.length > 0 && (
            <button
              onClick={() => setCourses([])}
              className="text-xs text-rose-400 hover:text-rose-300 font-medium transition"
            >
              Clear all
            </button>
          )}
        </div>

        {courses.length === 0 ? (
          <div className="bg-slate-900/40 border border-dashed border-slate-800 rounded-2xl p-12 text-center space-y-3">
            <BookOpen className="w-8 h-8 text-slate-600 mx-auto" />
            <p className="text-sm text-slate-400 font-medium">
              No courses recorded yet.
            </p>
            <p className="text-xs text-slate-500 max-w-md mx-auto">
              Select courses above or load one of the benchmark demo archetypes from the top menu to immediately explore recommendations.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {courses.map((c) => {
              const gradeInfo = getGradeInfo(c.mark);
              return (
                <div
                  key={c.course_code}
                  className="bg-slate-900/60 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 flex flex-col justify-between space-y-2 shadow-sm transition"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold text-indigo-300 font-mono">
                          {c.course_code}
                        </span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                          {c.credits} cr
                        </span>
                        {c.course_type && c.course_type !== 'Core' && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-violet-950/60 text-violet-300 border border-violet-800/40">
                            {c.course_type}
                          </span>
                        )}
                      </div>
                      <h3 className="text-xs font-semibold text-white mt-1 line-clamp-1">
                        {c.course_name}
                      </h3>
                      <p className="text-[11px] text-slate-400 mt-0.5">
                        {c.subject_area}
                      </p>
                    </div>

                    <button
                      onClick={() => handleRemoveCourse(c.course_code)}
                      className="text-slate-500 hover:text-rose-400 p-1 rounded-md hover:bg-slate-800 transition"
                      title="Remove course"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs">
                    <span className="text-slate-400 text-[11px]">
                      Score: <strong className="text-white">{c.mark}%</strong>
                    </span>
                    <span className={`px-2 py-0.5 rounded text-[11px] font-bold border ${gradeInfo.color}`}>
                      {gradeInfo.grade} ({gradeInfo.gp.toFixed(1)})
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-slate-800 flex items-center justify-between">
        <button
          onClick={onPrev}
          className="flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-white px-4 py-2 rounded-xl hover:bg-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Profile</span>
        </button>

        <button
          onClick={onNext}
          className="flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-600/25 transition"
        >
          <span>Proceed to Career Interests</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Custom Course Modal */}
      {isCustomModalOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-white">Add Custom Course</h3>
            <p className="text-xs text-slate-400">
              Enter course details from any curriculum or transfer credits.
            </p>

            <form onSubmit={handleAddCustomCourse} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 mb-1">Course Code</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. CS3050"
                  value={customCourse.code}
                  onChange={(e) => setCustomCourse({ ...customCourse, code: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                />
              </div>

              <div>
                <label className="block text-slate-300 mb-1">Course Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Distributed Cloud Architectures"
                  value={customCourse.name}
                  onChange={(e) => setCustomCourse({ ...customCourse, name: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 mb-1">Credits</label>
                  <input
                    type="number"
                    min="1"
                    max="6"
                    value={customCourse.credits}
                    onChange={(e) => setCustomCourse({ ...customCourse, credits: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  />
                </div>
                <div>
                  <label className="block text-slate-300 mb-1">Course Type</label>
                  <select
                    value={customCourse.courseType}
                    onChange={(e) => setCustomCourse({ ...customCourse, courseType: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                  >
                    <option value="Core">Core</option>
                    <option value="Elective">Elective</option>
                    <option value="NGPA">NGPA</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-slate-300 mb-1">Subject Taxonomy Area</label>
                <select
                  value={customCourse.subjectArea}
                  onChange={(e) => setCustomCourse({ ...customCourse, subjectArea: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                >
                  <option value="Programming & Software Development">Programming & Software Development</option>
                  <option value="Mathematics & Statistics">Mathematics & Statistics</option>
                  <option value="Database Systems">Database Systems</option>
                  <option value="Data Science & Analytics">Data Science & Analytics</option>
                  <option value="Artificial Intelligence">Artificial Intelligence</option>
                  <option value="Computer Networks">Computer Networks</option>
                  <option value="Cyber Security">Cyber Security</option>
                  <option value="Systems & Architecture">Systems & Architecture</option>
                  <option value="Web & Mobile Development">Web & Mobile Development</option>
                  <option value="Theoretical Computer Science">Theoretical Computer Science</option>
                  <option value="IT Management & Professional Practice">IT Management & Professional Practice</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-300 mb-1">Mark Earned (0 - 100%)</label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  step="0.5"
                  value={customCourse.mark}
                  onChange={(e) => setCustomCourse({ ...customCourse, mark: e.target.value })}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                />
              </div>

              <div className="pt-4 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setIsCustomModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2 rounded-xl font-semibold shadow-md shadow-indigo-600/20"
                >
                  Add Course
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
