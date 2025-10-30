"use client"
import React from 'react'
import clsx from 'clsx'

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost' | 'success' | 'danger'
}

export function Button({ className, variant = 'primary', ...props }: Props) {
  const base = 'inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition disabled:opacity-50 disabled:cursor-not-allowed'
  const styles: Record<string, string> = {
    primary: 'bg-brand text-white hover:bg-brand-dark',
    secondary: 'bg-bg.card text-textc-primary hover:bg-white/10 border border-white/10',
    ghost: 'text-textc-secondary hover:text-textc-primary hover:bg-white/5',
    success: 'bg-status-success text-white hover:brightness-110',
    danger: 'bg-status-error text-white hover:brightness-110',
  }
  return <button className={clsx(base, styles[variant], className)} {...props} />
}


