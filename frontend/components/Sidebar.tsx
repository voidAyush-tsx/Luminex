"use client"
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Grid, Upload, ShieldCheck, Download, Settings } from 'lucide-react'

const nav = [
  { label: 'Dashboard', href: '/dashboard', icon: Grid },
  { label: 'Upload', href: '/upload', icon: Upload },
  { label: 'Verify', href: '/verify', icon: ShieldCheck },
  { label: 'Export', href: '/export', icon: Download },
]

export default function Sidebar() {
  const pathname = usePathname()
  return (
    <aside className="fixed left-0 top-0 h-full w-[320px] bg-bg-primary text-textc-primary border-r border-white/5 flex flex-col">
      <div className="px-6 py-5 border-b border-white/5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded bg-brand" />
          <span className="text-lg font-semibold">Luminex</span>
        </div>
        <div className="text-right">
          <div className="text-sm">Ayush Ranjan</div>
          <div className="text-[10px] text-textc-secondary border border-white/10 rounded px-2 py-0.5 inline-block">Free</div>
        </div>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1">
        {nav.map(item => {
          const Icon = item.icon
          const active = pathname.startsWith(item.href)
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg transition ${active ? 'bg-brand text-white' : 'hover:bg-white/5 text-textc-secondary'}`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-sm font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>
      <div className="mt-auto p-3">
        <Link href="/settings" className={`flex items-center gap-3 px-3 py-2 rounded-lg transition ${pathname.startsWith('/settings') ? 'bg-brand text-white' : 'hover:bg-white/5 text-textc-secondary'}`}>
          <Settings className="w-5 h-5" />
          <span className="text-sm font-medium">Settings</span>
        </Link>
      </div>
    </aside>
  )
}


