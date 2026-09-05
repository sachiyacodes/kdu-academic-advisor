import React from 'react';

export default function Skeleton({ className = '', ...props }) {
  return (
    <div
      className={`animate-pulse bg-surface-elevated rounded-md ${className}`}
      {...props}
    />
  );
}
