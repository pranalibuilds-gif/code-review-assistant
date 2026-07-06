import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  className,
  isLoading,
  disabled,
  ...props
}) => {
  const variants = {
    primary: 'bg-primary-main text-white hover:bg-indigo-700 shadow-sm',
    secondary: 'bg-surface-card text-text-base border border-surface-border hover:bg-slate-50',
    danger: 'bg-status-error text-white hover:bg-red-700',
    ghost: 'bg-transparent text-text-muted hover:bg-slate-100 hover:text-text-base',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg',
  };

  return (
    <button
      className={twMerge(
        clsx(
          'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-primary-main focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
          variants[variant],
          sizes[size],
          className
        )
      )}
      disabled={isLoading || disabled}
      {...props}
    >
      {isLoading ? (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      ) : null}
      {children}
    </button>
  );
};

export default Button;
