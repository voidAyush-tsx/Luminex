"use client"
import React, { createContext, useContext, useState } from 'react'

interface AppContextType {
  apiBaseUrl: string
  setApiBaseUrl: (url: string) => void
}

const AppContext = createContext<AppContextType>({
  apiBaseUrl: 'http://127.0.0.1:8000',
  setApiBaseUrl: () => {},
})

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [apiBaseUrl, setApiBaseUrl] = useState('http://127.0.0.1:8000')

  return (
    <AppContext.Provider value={{ apiBaseUrl, setApiBaseUrl }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)


