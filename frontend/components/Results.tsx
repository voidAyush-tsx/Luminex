"use client"
import React from 'react'

type Props = {
  data: any | null
}

function Section({ title, children }: { title: string, children: React.ReactNode }) {
  return (
    <div className="border rounded p-4">
      <h3 className="font-semibold mb-2">{title}</h3>
      <div className="text-sm text-gray-700 overflow-x-auto">{children}</div>
    </div>
  )
}

export default function Results({ data }: Props) {
  if (!data) return null
  return (
    <div className="space-y-4">
      <Section title="AI Comparison">
        <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(data.ai_result, null, 2)}</pre>
      </Section>
      <Section title="Rule-based Comparison">
        <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(data.rule_result, null, 2)}</pre>
      </Section>
      <Section title="Structured - Invoice">
        <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(data.invoice_structured, null, 2)}</pre>
      </Section>
      <Section title="Structured - PO">
        <pre className="text-xs whitespace-pre-wrap">{JSON.stringify(data.po_structured, null, 2)}</pre>
      </Section>
    </div>
  )
}


