import React from 'react';
import { ChevronDown } from 'lucide-react';

export default function Select({
  label,
  error,
  helperText,
  id,
  options = [],
  children,
  className = '',
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
        <select
          id={id}
          className={`h-11 w-full appearance-none rounded-lg bg-bg-secondary border text-text-primary text-sm pl-3.5 pr-10 ${
            error
              ? 'border-danger focus:border-danger focus:ring-danger/20'
              : 'border-border focus:border-primary focus:ring-primary/20'
          } focus:outline-none focus:ring-2 transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer ${className}`}
          {...props}
        >
          {children
            ? children
            : options.map((opt) => (
                <option
                  key={typeof opt === 'object' ? opt.value : opt}
                  value={typeof opt === 'object' ? opt.value : opt}
                  className="bg-surface text-text-primary"
                >
                  {typeof opt === 'object' ? opt.label : opt}
                </option>
              ))}
        </select>
        <div className="absolute right-3.5 text-text-muted pointer-events-none">
          <ChevronDown className="w-4 h-4" />
        </div>
      </div>
      {error && <span className="text-xs text-danger font-medium">{error}</span>}
      {helperText && !error && (
        <span className="text-xs text-text-muted">{helperText}</span>
      )}
    </div>
  );
}
