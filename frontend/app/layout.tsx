import './globals.css'
import { ReactNode } from 'react'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import { AppProvider } from '../components/AppContext'

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
          <header className="border-b">
            <div className="container flex items-center justify-between py-4">
              <Link href="/" className="font-semibold text-lg">Luminex</Link>
              <nav className="flex gap-4 text-sm">
                <Link href="/" className="hover:underline">Upload</Link>
                <Link href="/history" className="hover:underline">History</Link>
                <Link href="/stats" className="hover:underline">Stats</Link>
              </nav>
            </div>
          </header>
          <main className="container py-6">
            {children}
          </main>
        </AppProvider>
      </body>
    </html>
  )
}


