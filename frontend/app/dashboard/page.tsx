"use client"
import React, { useEffect, useMemo, useState } from 'react'
import { useApp } from '../../components/AppContext'
import { Card, CardBody } from '../../components/ui/Card'

export default function DashboardPage() {
  const { apiBaseUrl } = useApp()
  const [stats, setStats] = useState<any | null>(null)
  const [recent, setRecent] = useState<any[]>([])

  useEffect(() => {
    ;(async () => {
      try {
        const [s, h] = await Promise.all([
          fetch(`${apiBaseUrl}/stats`).then(r => r.json()),
          fetch(`${apiBaseUrl}/history?limit=6`).then(r => r.json()),
        ])
        setStats(s)
        setRecent(h.transactions || [])
      } catch {}
    })()
  }, [apiBaseUrl])

  const formattedAmount = useMemo(() => {
    const total = recent.reduce((sum, t) => sum + (Number(t.invoice_total) || 0), 0)
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(total)
  }, [recent])

  return (
    <div className="space-y-8">
      <h1 className="text-4xl md:text-5xl font-semibold">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <StatCard title="Total Documents" value={stats?.total_processed ?? 0} />
        <StatCard title="Amount Processed" value={formattedAmount} />
        <StatCard title="Verified" value={stats?.matched ?? 0} />
        <StatCard title="Pending Review" value={Math.max((stats?.mismatched ?? 0), 0)} />
      </div>

      <div className="space-y-3">
        <h2 className="text-2xl text-textc-secondary">Recent Activity</h2>
        <Card>
          <CardBody>
            {recent.length === 0 ? (
              <div className="h-32 flex items-center justify-center text-textc-secondary">No recent activity</div>
            ) : (
              <ul className="divide-y divide-white/10">
                {recent.map((t, i) => (
                  <li key={i} className="py-3 flex items-center justify-between">
                    <div className="text-sm">
                      <div className="text-textc-primary">{t.invoice_vendor || 'Unknown'} → {t.po_vendor || 'Unknown'}</div>
                      <div className="text-textc-secondary">{t.timestamp}</div>
                    </div>
                    <div className="text-sm">{t.status}</div>
                  </li>
                ))}
              </ul>
            )}
          </CardBody>
        </Card>
      </div>
    </div>
  )
}

function StatCard({ title, value }: { title: string, value: any }) {
  return (
    <Card>
      <CardBody>
        <div className="text-lg">{title}</div>
        <div className="text-4xl md:text-5xl font-bold mt-2">{value}</div>
      </CardBody>
    </Card>
  )
}


