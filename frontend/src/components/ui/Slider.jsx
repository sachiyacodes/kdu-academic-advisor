import React from 'react';

export default function Slider({
  min = 1,
  max = 5,
  step = 0.5,
  value,
  onChange,
  label,
  valueDisplay,
  helperText,
  className = '',
  ...props
}) {
  const numericValue = typeof value === 'number' ? value : parseFloat(value) || min;
  const percentage = Math.min(100, Math.max(0, ((numericValue - min) / (max - min)) * 100));

  return (
    <div className={`flex flex-col gap-2 w-full ${className}`}>
      {(label || valueDisplay !== undefined) && (
        <div className="flex items-center justify-between">
          {label && (
            <span className="text-sm font-medium text-text-primary">{label}</span>
          )}
          {valueDisplay !== undefined && (
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-primary-subtle text-primary border border-primary-border">
              {valueDisplay}
            </span>
          )}
        </div>
      )}
      <div className="relative flex items-center h-6">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={numericValue}
          onChange={onChange}
          className="w-full h-1.5 bg-border rounded-full appearance-none cursor-pointer focus-ring accent-primary"
          style={{
            background: `linear-gradient(to right, var(--color-primary) 0%, var(--color-primary) ${percentage}%, var(--color-border) ${percentage}%, var(--color-border) 100%)`,
          }}
          {...props}
        />
      </div>
      {helperText && <span className="text-xs text-text-muted">{helperText}</span>}
    </div>
  );
}
