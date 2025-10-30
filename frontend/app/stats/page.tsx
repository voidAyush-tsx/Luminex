"use client"
import React, { useEffect, useState } from 'react'
import { useApp } from '../../components/AppContext'

export default function StatsPage() {
  const { apiBaseUrl } = useApp()
  const [data, setData] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetch(`${apiBaseUrl}/stats`)
        if (!res.ok) throw new Error(await res.text())
        setData(await res.json())
      } catch (e: any) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [apiBaseUrl])

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Stats</h1>
      {loading && <div>Loading…</div>}
      {error && <div className="text-red-600 text-sm">{error}</div>}
      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard label="Total Processed" value={data.total_processed} />
          <StatCard label="Matched" value={data.matched} />
          <StatCard label="Mismatched" value={data.mismatched} />
          <StatCard label="Match Rate" value={data.match_rate} />
        </div>
      )}
    </div>
  )
}

function StatCard({ label, value }: { label: string, value: any }) {
  return (
    <div className="border rounded p-4">
      <div className="text-sm text-gray-500">{label}</div>
      <div className="text-2xl font-semibold">{value}</div>
    </div>
  )
}


