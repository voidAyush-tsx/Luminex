import React from 'react'
import { Badge } from './ui/Badge'

interface Row {
  field: string
  invoiceValue: any
  poValue: any
  match: boolean
  difference?: string
}

export function ComparisonTable({ rows, confidence }: { rows: Row[], confidence: number }) {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-xl font-semibold">Confidence Score</span>
          <span className="text-3xl font-bold">{confidence} %</span>
        </div>
        <div className="w-full h-3 bg-bg-secondary rounded-full overflow-hidden">
          <div className="h-full bg-brand rounded-full" style={{ width: `${Math.max(0, Math.min(100, confidence))}%` }} />
        </div>
      </div>

      <div className="bg-bg-card rounded-xl p-6">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/10">
              <th className="text-left p-3 uppercase text-xs text-textc-secondary">Feild</th>
              <th className="text-center p-3 uppercase text-xs text-textc-secondary">Invoice</th>
              <th className="text-center p-3 uppercase text-xs text-textc-secondary">Purchase Order</th>
              <th className="text-right p-3 uppercase text-xs text-textc-secondary">Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.field} className={`border-b border-white/5 ${!r.match ? 'border-l-4 border-l-status-error' : ''}`}>
                <td className="p-3 text-sm">{r.field}</td>
                <td className="p-3 text-sm text-center">{formatVal(r.invoiceValue)}</td>
                <td className="p-3 text-sm text-center">{formatVal(r.poValue)}</td>
                <td className="p-3 text-sm text-right">
                  {r.match ? (
                    <Badge color="success">Match</Badge>
                  ) : r.difference ? (
                    <span className="text-status-error font-medium">{r.difference}</span>
                  ) : (
                    <Badge color="error">Error</Badge>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function formatVal(v: any) {
  if (v === null || v === undefined || v === '') return '—'
  return String(v)
}


