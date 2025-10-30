"use client"
import React, { createContext, useContext, useMemo, useState } from 'react'

type AppContextType = {
  apiBaseUrl: string
  setApiBaseUrl: (v: string) => void
}

const AppContext = createContext<AppContextType | undefined>(undefined)

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [apiBaseUrl, setApiBaseUrl] = useState<string>(process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000')
  const value = useMemo(() => ({ apiBaseUrl, setApiBaseUrl }), [apiBaseUrl])
  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used within AppProvider')
  return ctx
}


