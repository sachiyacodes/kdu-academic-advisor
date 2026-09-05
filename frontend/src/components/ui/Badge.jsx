import React from 'react';

export default function Badge({
  children,
  variant = 'neutral',
  size = 'md',
  icon: Icon,
  className = '',
  ...props
}) {
  const baseClasses = 'inline-flex items-center font-medium rounded-full border transition-colors';

  const sizeClasses = {
    sm: 'text-[11px] leading-tight px-2 py-0.5 gap-1',
    md: 'text-xs leading-none px-2.5 py-1 gap-1.5',
  };

  const variantClasses = {
    primary: 'bg-primary-subtle border-primary-border text-primary',
    teal: 'bg-teal-subtle border-teal-border text-teal',
    success: 'bg-success-subtle border-success-border text-success',
    warning: 'bg-warning-subtle border-warning-border text-warning',
    danger: 'bg-danger-subtle border-danger-border text-danger',
    info: 'bg-info-subtle border-info/30 text-info',
    neutral: 'bg-surface border-border text-text-secondary',
  };

  return (
    <span
      className={`${baseClasses} ${sizeClasses[size] || sizeClasses.md} ${variantClasses[variant] || variantClasses.neutral} ${className}`}
      {...props}
    >
      {Icon && <Icon className="w-3 h-3 shrink-0" />}
      {children}
    </span>
  );
}
