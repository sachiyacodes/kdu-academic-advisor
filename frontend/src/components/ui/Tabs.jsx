import React from 'react';

export default function Tabs({
  tabs = [],
  activeTab,
  onChange,
  className = '',
}) {
  return (
    <div
      role="tablist"
      className={`inline-flex p-1 rounded-lg bg-bg-secondary border border-border gap-1 overflow-x-auto max-w-full ${className}`}
    >
      {tabs.map((tab) => {
        const id = typeof tab === 'object' ? tab.id : tab;
        const label = typeof tab === 'object' ? tab.label : tab;
        const Icon = typeof tab === 'object' ? tab.icon : null;
        const count = typeof tab === 'object' ? tab.count : undefined;
        const isActive = activeTab === id;

        return (
          <button
            key={id}
            role="tab"
            type="button"
            aria-selected={isActive}
            onClick={() => onChange && onChange(id)}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs md:text-sm font-medium transition-all duration-150 whitespace-nowrap cursor-pointer select-none focus-ring ${
              isActive
                ? 'bg-surface text-text-primary shadow-xs border border-border font-semibold'
                : 'text-text-secondary hover:text-text-primary hover:bg-surface-hover border border-transparent'
            }`}
          >
            {Icon && <Icon className="w-3.5 h-3.5 shrink-0" />}
            <span>{label}</span>
            {count !== undefined && (
              <span
                className={`text-[11px] px-1.5 py-0.5 rounded-full ${
                  isActive
                    ? 'bg-primary-subtle text-primary'
                    : 'bg-surface-hover text-text-muted'
                }`}
              >
                {count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
