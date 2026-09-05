import React from 'react';

export default function Card({
  children,
  variant = 'default',
  padding = 'normal',
  className = '',
  onClick,
  ...props
}) {
  const baseClasses = 'rounded-xl border transition-all duration-150';

  const variantClasses = {
    default: 'bg-surface border-border',
    elevated: 'bg-surface-elevated border-border shadow-sm',
    interactive:
      'bg-surface border-border hover:bg-surface-hover hover:border-primary/40 cursor-pointer',
    teal: 'bg-surface border-teal-border/40',
  };

  const paddingClasses = {
    none: 'p-0',
    sm: 'p-3 md:p-4',
    normal: 'p-5 md:p-6',
    lg: 'p-6 md:p-8',
  };

  return (
    <div
      onClick={onClick}
      className={`${baseClasses} ${variantClasses[variant] || variantClasses.default} ${paddingClasses[padding] || paddingClasses.normal} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
