import React from 'react';

export default function IconButton({
  icon: Icon,
  label,
  variant = 'ghost',
  size = 'md',
  className = '',
  onClick,
  disabled = false,
  ...props
}) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-9 h-9',
    lg: 'w-10 h-10',
  };

  const iconSizes = {
    sm: 'w-3.5 h-3.5',
    md: 'w-4 h-4',
    lg: 'w-4.5 h-4.5',
  };

  const variantClasses = {
    ghost:
      'text-text-secondary hover:text-text-primary hover:bg-surface-hover active:bg-surface-elevated',
    secondary:
      'bg-surface border border-border text-text-secondary hover:text-text-primary hover:bg-surface-hover',
    destructive:
      'text-text-muted hover:text-danger hover:bg-danger-subtle hover:border-danger-border border border-transparent',
  };

  return (
    <button
      type="button"
      aria-label={label}
      title={label}
      disabled={disabled}
      onClick={onClick}
      className={`inline-flex items-center justify-center rounded-lg transition-colors duration-150 focus-ring disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer ${
        sizeClasses[size] || sizeClasses.md
      } ${variantClasses[variant] || variantClasses.ghost} ${className}`}
      {...props}
    >
      {Icon && <Icon className={iconSizes[size] || iconSizes.md} />}
    </button>
  );
}
