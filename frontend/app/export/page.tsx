"use client"
import React from 'react'
import { Card, CardBody, CardTitle } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { useApp } from '../../components/AppContext'

export default function ExportPage() {
  const { apiBaseUrl } = useApp()
  return (
    <div className="space-y-8">
      <h1 className="text-4xl md:text-5xl font-semibold">Export</h1>

      <Card>
        <CardBody>
          <CardTitle>Filters</CardTitle>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-textc-secondary">
            <div className="flex gap-3 items-center">
              <div className="w-28">Date Range</div>
              <input type="date" className="bg-bg-secondary rounded px-3 py-2" />
              <input type="date" className="bg-bg-secondary rounded px-3 py-2" />
            </div>
            <div className="flex gap-3 items-center">
              <div className="w-28">Status</div>
              <select className="bg-bg-secondary rounded px-3 py-2">
                <option>All</option>
                <option>Verified</option>
                <option>Pending</option>
                <option>Flagged</option>
                <option>Error</option>
              </select>
            </div>
          </div>
          <div className="mt-4 flex gap-3">
            <Button>Apply Filters</Button>
            <Button variant="secondary">Reset</Button>
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <CardTitle>Export Format</CardTitle>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-bg-secondary rounded-xl p-4 space-y-3">
              <div className="font-semibold">Standard CSV</div>
              <div className="text-sm text-textc-secondary">All fields in comma-separated format</div>
              <Button as-child>
                {/* @ts-ignore */}
                <a href={`${apiBaseUrl}/export`}>Download CSV</a>
              </Button>
            </div>
            <div className="bg-bg-secondary rounded-xl p-4 space-y-3 opacity-70 pointer-events-none">
              <div className="font-semibold">Excel Workbook</div>
              <div className="text-sm text-textc-secondary">Formatted Excel with multiple sheets</div>
              <Button disabled>Download Excel</Button>
            </div>
            <div className="bg-bg-secondary rounded-xl p-4 space-y-3 opacity-70 pointer-events-none">
              <div className="font-semibold">PDF Report</div>
              <div className="text-sm text-textc-secondary">Formatted report with charts</div>
              <Button variant="danger" disabled>Download PDF</Button>
            </div>
          </div>
        </CardBody>
      </Card>
    </div>
  )
}


