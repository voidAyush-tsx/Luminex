"use client"
import React, { useEffect, useState } from 'react'
import { useApp } from '../../components/AppContext'

export default function HistoryPage() {
  const { apiBaseUrl } = useApp()
  const [data, setData] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    async function load() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetch(`${apiBaseUrl}/history?limit=20`)
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
      <h1 className="text-2xl font-semibold">History</h1>
      <div className="flex items-center gap-2">
        <a
          href={`${apiBaseUrl}/export`}
          className="bg-brand text-white text-sm px-3 py-2 rounded"
        >
          Export CSV
        </a>
      </div>
      {loading && <div>Loading…</div>}
      {error && <div className="text-red-600 text-sm">{error}</div>}
      {data && (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm border">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left p-2 border">Time</th>
                <th className="text-left p-2 border">Invoice Vendor</th>
                <th className="text-left p-2 border">PO Vendor</th>
                <th className="text-left p-2 border">Invoice Total</th>
                <th className="text-left p-2 border">PO Total</th>
                <th className="text-left p-2 border">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.transactions?.map((t: any, idx: number) => (
                <tr key={idx} className="odd:bg-white even:bg-gray-50">
                  <td className="p-2 border whitespace-nowrap">{t.timestamp}</td>
                  <td className="p-2 border">{t.invoice_vendor}</td>
                  <td className="p-2 border">{t.po_vendor}</td>
                  <td className="p-2 border">{t.invoice_total}</td>
                  <td className="p-2 border">{t.po_total}</td>
                  <td className="p-2 border">{t.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}


