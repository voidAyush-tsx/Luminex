import React from 'react'
import clsx from 'clsx'

export function Card({ className, children }: { className?: string, children: React.ReactNode }) {
  return (
    <div className={clsx('bg-bg-card rounded-xl border border-white/10', className)}>
      {children}
    </div>
  )
}

export function CardBody({ className, children }: { className?: string, children: React.ReactNode }) {
  return <div className={clsx('p-6', className)}>{children}</div>
}

export function CardTitle({ className, children }: { className?: string, children: React.ReactNode }) {
  return <h3 className={clsx('text-textc-primary text-lg font-semibold', className)}>{children}</h3>
}


