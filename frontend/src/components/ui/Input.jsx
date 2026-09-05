import React from 'react';

export default function Input({
  label,
  error,
  helperText,
  id,
  className = '',
  icon: Icon,
  ...props
}) {
  return (
    <div className="flex flex-col gap-1.5 w-full">
      {label && (
        <label htmlFor={id} className="text-xs font-semibold text-text-secondary">
          {label}
        </label>
      )}
      <div className="relative flex items-center">
        {Icon && (
          <div className="absolute left-3.5 text-text-muted pointer-events-none">
            <Icon className="w-4 h-4" />
          </div>
        )}
        <input
          id={id}
          className={`h-11 w-full rounded-lg bg-bg-secondary border text-text-primary text-sm px-3.5 ${
            Icon ? 'pl-10' : ''
          } ${
            error
              ? 'border-danger focus:border-danger focus:ring-danger/20'
              : 'border-border focus:border-primary focus:ring-primary/20'
          } placeholder:text-text-muted focus:outline-none focus:ring-2 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
          {...props}
        />
      </div>
      {error && <span className="text-xs text-danger font-medium">{error}</span>}
      {helperText && !error && (
        <span className="text-xs text-text-muted">{helperText}</span>
      )}
    </div>
  );
}
