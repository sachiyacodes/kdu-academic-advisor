import React from 'react';
import { Compass, Sparkles, ArrowRight, ArrowLeft, RotateCcw, Check } from 'lucide-react';

export default function StepInterests({
  interests,
  setInterests,
  catalogInterests,
  onPrev,
  onNext,
}) {
  const activeCount = Object.keys(interests).length;

  const handleIntensityChange = (subjectArea, value) => {
    const val = parseFloat(value);
    if (val === 0) {
      const updated = { ...interests };
      delete updated[subjectArea];
      setInterests(updated);
    } else {
      setInterests({ ...interests, [subjectArea]: val });
    }
  };

  const applyPreset = (presetMap) => {
    setInterests(presetMap);
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="border-b border-slate-800 pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-indigo-400 text-xs font-semibold uppercase tracking-wider mb-1">
            <span>Step 3 of 6</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Career Interests & Preferences
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Calibrate your personal aspirations. The hybrid engine weights your interest intensity (1.0 - 5.0) alongside academic performance.
          </p>
        </div>

        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 rounded-xl px-4 py-2 text-xs">
          <span className="text-slate-400">Active Interests:</span>
          <span className="font-bold text-indigo-400">{activeCount} / {catalogInterests.length}</span>
        </div>
      </div>

      {/* Quick Presets */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-4 space-y-2.5">
        <span className="text-xs font-semibold text-slate-300 flex items-center space-x-1.5">
          <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
          <span>Quick Alignment Presets:</span>
        </span>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() =>
              applyPreset({
                'Data Science & Analytics': 5.0,
                'Mathematics & Statistics': 4.5,
                'Artificial Intelligence': 4.0,
                'Database Systems': 3.5,
              })
            }
            className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-700/40 transition"
          >
            📊 Data Science & AI Focus
          </button>
          <button
            type="button"
            onClick={() =>
              applyPreset({
                'Cyber Security': 5.0,
                'Computer Networks': 4.5,
                'Systems & Architecture': 4.0,
              })
            }
            className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-700/40 transition"
          >
            🛡️ Cyber Security & Networks
          </button>
          <button
            type="button"
            onClick={() =>
              applyPreset({
                'Programming & Software Development': 5.0,
                'Systems & Architecture': 4.5,
                'Database Systems': 4.0,
                'Web & Mobile Development': 4.0,
              })
            }
            className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-700/40 transition"
          >
            💻 Software Engineering
          </button>
          <button
            type="button"
            onClick={() => setInterests({})}
            className="text-xs px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-400 border border-slate-700 transition"
          >
            Clear All
          </button>
        </div>
      </div>

      {/* Interests Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {catalogInterests.map((item) => {
          const area = item.subject_area || item.name;
          const currentIntensity = interests[area] || 0;
          const isSelected = currentIntensity > 0;

          return (
            <div
              key={item.interest_id}
              className={`rounded-2xl p-4 border transition flex flex-col justify-between space-y-4 ${
                isSelected
                  ? 'bg-slate-900 border-indigo-500/50 shadow-lg shadow-indigo-500/5'
                  : 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700'
              }`}
            >
              <div>
                <div className="flex items-start justify-between">
                  <h3 className="text-xs font-bold text-white">
                    {item.name}
                  </h3>
                  {isSelected && (
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      {currentIntensity.toFixed(1)} / 5.0
                    </span>
                  )}
                </div>
                <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">
                  {item.description || `Explore concepts in ${area}`}
                </p>
              </div>

              {/* Slider Control */}
              <div className="space-y-1.5 pt-2 border-t border-slate-800/80">
                <div className="flex justify-between text-[10px] text-slate-500">
                  <span>None (0)</span>
                  <span className={isSelected ? 'text-indigo-400 font-semibold' : ''}>
                    {currentIntensity === 0
                      ? 'Not Selected'
                      : currentIntensity >= 4.5
                      ? 'Core Passion'
                      : currentIntensity >= 3.5
                      ? 'High Interest'
                      : currentIntensity >= 2.5
                      ? 'Moderate'
                      : 'Slight'}
                  </span>
                  <span>Passionate (5.0)</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="5"
                  step="0.5"
                  value={currentIntensity}
                  onChange={(e) => handleIntensityChange(area, e.target.value)}
                  className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Navigation Controls */}
      <div className="pt-6 border-t border-slate-800 flex items-center justify-between">
        <button
          onClick={onPrev}
          className="flex items-center space-x-2 text-xs font-semibold text-slate-400 hover:text-white px-4 py-2 rounded-xl hover:bg-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Course History</span>
        </button>

        <button
          onClick={onNext}
          className="flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 text-white text-xs font-semibold px-6 py-2.5 rounded-xl shadow-lg shadow-indigo-600/25 transition"
        >
          <span>Generate Recommendations</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
