import React from 'react';

export default function Skeleton({ className = '', style = {}, ...props }) {
  return (
    <div
      className={className}
      style={{
        background: 'var(--color-surface-elevated)',
        borderRadius: '6px',
        animation: 'pulse 1.5s ease-in-out infinite',
        ...style,
      }}
      {...props}
    />
  );
}
