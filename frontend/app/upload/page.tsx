"use client"
import React, { useState } from 'react'
import { FileUpload } from '../../components/FileUpload'
import { Button } from '../../components/ui/Button'
import { useApp } from '../../components/AppContext'
import { useRouter } from 'next/navigation'

export default function UploadPage() {
  const { apiBaseUrl } = useApp()
  const router = useRouter()
  const [invoice, setInvoice] = useState<File | null>(null)
  const [po, setPo] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleProceed() {
    if (!invoice || !po) return
    setLoading(true)
    setError(null)
    try {
      const form = new FormData()
      form.append('invoice', invoice)
      form.append('po', po)
      const res = await fetch(`${apiBaseUrl}/upload_advanced`, { method: 'POST', body: form })
      if (!res.ok) throw new Error(await res.text())
      const json = await res.json()
      sessionStorage.setItem('luminex:lastResult', JSON.stringify(json))
      router.push('/verify')
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <h1 className="text-4xl md:text-5xl font-semibold">Upload</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <FileUpload title="Invoice" onFileSelect={setInvoice} />
        <FileUpload title="Purchase Order" onFileSelect={setPo} />
      </div>
      {error && <div className="text-status-error text-sm">{error}</div>}
      <div>
        <Button onClick={handleProceed} disabled={!invoice || !po || loading}>
          {loading ? 'Processing…' : 'Proceed to Verify'}
        </Button>
      </div>
    </div>
  )
}


