"use client"
import React, { useMemo } from 'react'
import { ComparisonTable } from '../../components/ComparisonTable'
import { Button } from '../../components/ui/Button'

export default function VerifyPage() {
  const result = useMemo(() => {
    const raw = typeof window !== 'undefined' ? sessionStorage.getItem('luminex:lastResult') : null
    return raw ? JSON.parse(raw) : null
  }, [])

  const rows = useMemo(() => {
    const ai = result?.ai_result
    const comps = ai?.field_comparisons || []
    return comps.map((c: any) => ({
      field: normalizeField(c.field),
      invoiceValue: c.invoice_value,
      poValue: c.po_value,
      match: !!c.match,
      difference: diffString(c)
    }))
  }, [result])

  const confidence = Number(result?.ai_result?.confidence_score ?? 0)

  return (
    <div className="space-y-8">
      <h1 className="text-4xl md:text-5xl font-semibold">Verify</h1>
      <ComparisonTable rows={rows} confidence={confidence} />
      <div className="flex gap-3">
        <Button variant="primary">Approve & Save</Button>
        <Button variant="secondary">Flag for Review</Button>
        <Button variant="ghost">Re-upload</Button>
      </div>
    </div>
  )
}

function normalizeField(f: string) {
  if (!f) return '—'
  const map: Record<string, string> = {
    vendor_name: 'Vendor',
    total_amount: 'Total',
    date: 'Date',
    quantity: 'Quantity',
    unit_price: 'Unit Price',
    service_description: 'Service',
    tax_amount: 'Tax'
  }
  return map[f] || f
}

function diffString(c: any) {
  if (c.difference === null || c.difference === undefined) return undefined
  const n = Number(c.difference)
  if (!isFinite(n)) return undefined
  const sign = n >= 0 ? '+ ' : '- '
  return `${sign}$ ${Math.abs(n).toLocaleString()}`
}


