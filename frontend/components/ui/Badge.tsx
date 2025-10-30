import React from 'react'
import clsx from 'clsx'

export function Badge({ children, color = 'success' }: { children: React.ReactNode, color?: 'success' | 'error' | 'warning' }) {
  const styles: Record<string, string> = {
    success: 'bg-status-success/20 text-status-success border-status-success/30',
    error: 'bg-status-error/20 text-status-error border-status-error/30',
    warning: 'bg-status-warning/20 text-status-warning border-status-warning/30',
  }
  return (
    <span className={clsx('text-xs px-3 py-1 rounded-full border', styles[color])}>{children}</span>
  )
}


