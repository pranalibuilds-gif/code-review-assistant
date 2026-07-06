import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

const Card = ({ children, className, ...props }) => {
  return (
    <div
      className={twMerge(
        clsx(
          'bg-surface-card rounded-[28px] border border-surface-border shadow-soft overflow-hidden',
          className
        )
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
