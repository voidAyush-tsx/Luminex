"use client"
import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Loader2 } from 'lucide-react'
import { useApp } from './AppContext'

type Props = {
  onResult: (data: any) => void
}

export default function UploadForm({ onResult }: Props) {
  const { apiBaseUrl } = useApp()
  const [invoiceFile, setInvoiceFile] = useState<File | null>(null)
  const [poFile, setPoFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onDropInvoice = useCallback((accepted: File[]) => {
    setInvoiceFile(accepted[0] || null)
  }, [])

  const onDropPo = useCallback((accepted: File[]) => {
    setPoFile(accepted[0] || null)
  }, [])

  const { getRootProps: getInvoiceRoot, getInputProps: getInvoiceInput, isDragActive: isInvoiceActive } = useDropzone({ onDrop: onDropInvoice, multiple: false, accept: { 'application/pdf': ['.pdf'], 'image/*': ['.png', '.jpg', '.jpeg'] } })
  const { getRootProps: getPoRoot, getInputProps: getPoInput, isDragActive: isPoActive } = useDropzone({ onDrop: onDropPo, multiple: false, accept: { 'application/pdf': ['.pdf'], 'image/*': ['.png', '.jpg', '.jpeg'] } })

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    if (!invoiceFile || !poFile) {
      setError('Please select both Invoice and PO files')
      return
    }
    setLoading(true)
    try {
      const form = new FormData()
      form.append('invoice', invoiceFile)
      form.append('po', poFile)
      const res = await fetch(`${apiBaseUrl}/upload_advanced`, { method: 'POST', body: form })
      if (!res.ok) throw new Error(await res.text())
      const json = await res.json()
      onResult(json)
    } catch (err: any) {
      setError(err.message || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div {...getInvoiceRoot()} className={`border-2 border-dashed rounded p-6 text-center cursor-pointer ${isInvoiceActive ? 'border-brand' : 'border-gray-300'}`}>
          <input {...getInvoiceInput()} />
          <div className="flex flex-col items-center gap-2">
            <Upload className="w-6 h-6 text-brand" />
            <p className="text-sm">Drop or click to upload Invoice (PDF/PNG/JPG)</p>
            {invoiceFile && <p className="text-xs text-gray-500">{invoiceFile.name}</p>}
          </div>
        </div>
        <div {...getPoRoot()} className={`border-2 border-dashed rounded p-6 text-center cursor-pointer ${isPoActive ? 'border-brand' : 'border-gray-300'}`}>
          <input {...getPoInput()} />
          <div className="flex flex-col items-center gap-2">
            <Upload className="w-6 h-6 text-brand" />
            <p className="text-sm">Drop or click to upload Purchase Order (PDF/PNG/JPG)</p>
            {poFile && <p className="text-xs text-gray-500">{poFile.name}</p>}
          </div>
        </div>
      </div>
      {error && <div className="text-red-600 text-sm">{error}</div>}
      <button type="submit" disabled={loading} className="inline-flex items-center gap-2 bg-brand text-white px-4 py-2 rounded disabled:opacity-50">
        {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
        <span>{loading ? 'Processing…' : 'Process'}</span>
      </button>
    </form>
  )
}


