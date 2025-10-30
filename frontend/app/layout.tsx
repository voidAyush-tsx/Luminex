import './globals.css'
import { ReactNode } from 'react'
import { Inter } from 'next/font/google'
import { AppProvider } from '../components/AppContext'
import Sidebar from '../components/Sidebar'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Luminex - Invoice & PO Verification',
  description: 'AI-powered verification using Shivaay AI',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AppProvider>
          <Sidebar />
          <main className="pl-[320px] min-h-screen">
            <div className="max-w-7xl mx-auto px-8 py-8">
              {children}
            </div>
          </main>
        </AppProvider>
      </body>
    </html>
  )
}


