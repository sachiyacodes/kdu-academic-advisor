import React from 'react';

export default function EmptyState({
  icon: Icon,
  title,
  description,
  action,
  className = '',
}) {
  return (
    <div
      className={`flex flex-col items-center justify-center text-center p-8 md:p-12 rounded-xl border border-dashed border-border bg-bg-secondary/40 ${className}`}
    >
      {Icon && (
        <div className="w-12 h-12 rounded-full bg-surface-elevated border border-border flex items-center justify-center text-text-secondary mb-3.5">
          <Icon className="w-6 h-6" />
        </div>
      )}
      {title && (
        <h3 className="text-base font-semibold text-text-primary mb-1">
          {title}
        </h3>
      )}
      {description && (
        <p className="text-xs md:text-sm text-text-secondary max-w-sm mb-5 leading-relaxed">
          {description}
        </p>
      )}
      {action && <div>{action}</div>}
    </div>
  );
}
