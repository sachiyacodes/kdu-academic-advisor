import React from 'react';
import { Loader2 } from 'lucide-react';

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  icon: Icon,
  iconPosition = 'left',
  className = '',
  type = 'button',
  onClick,
  ...props
}) {
  const baseClasses =
    'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-150 select-none cursor-pointer focus-ring disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none active:scale-[0.99]';

  const sizeClasses = {
    sm: 'h-8 px-3 text-xs gap-1.5',
    md: 'h-10 px-4 text-sm gap-2',
    lg: 'h-11 px-5 text-sm md:text-base gap-2.5',
  };

  const variantClasses = {
    primary:
      'bg-primary text-white hover:bg-primary-hover active:bg-primary-active border border-primary/20 shadow-xs',
    secondary:
      'bg-surface text-text-primary hover:bg-surface-hover active:bg-surface-elevated border border-border',
    ghost:
      'bg-transparent text-text-secondary hover:text-text-primary hover:bg-surface-hover border border-transparent',
    destructive:
      'bg-surface text-danger hover:bg-danger-subtle hover:border-danger-border border border-border active:bg-danger/20',
    teal:
      'bg-teal text-white hover:bg-teal-hover border border-teal/20 shadow-xs',
  };

  return (
    <button
      type={type}
      disabled={disabled || loading}
      aria-busy={loading}
      onClick={onClick}
      className={`${baseClasses} ${sizeClasses[size] || sizeClasses.md} ${variantClasses[variant] || variantClasses.primary} ${className}`}
      {...props}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 animate-spin shrink-0" />
      ) : Icon && iconPosition === 'left' ? (
        <Icon className="w-4 h-4 shrink-0" />
      ) : null}
      <span>{children}</span>
      {!loading && Icon && iconPosition === 'right' ? (
        <Icon className="w-4 h-4 shrink-0" />
      ) : null}
    </button>
  );
}
