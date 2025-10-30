"use client"
import React, { useMemo, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, CheckCircle, XCircle } from 'lucide-react'

interface FileUploadProps {
  title: string
  onFileSelect: (file: File | null) => void
}

export function FileUpload({ title, onFileSelect }: FileUploadProps) {
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [file, setFile] = useState<File | null>(null)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg']
    },
    maxSize: 10 * 1024 * 1024,
    multiple: false,
    onDrop: (accepted) => {
      const f = accepted[0]
      if (!f) return
      setStatus('uploading')
      // Simulate quick validation
      setTimeout(() => {
        setFile(f)
        onFileSelect(f)
        setStatus('success')
      }, 200)
    },
    onDropRejected: () => {
      setStatus('error')
    }
  })

  const borderClass = useMemo(() => {
    if (status === 'success') return 'border-green-500'
    if (status === 'error') return 'border-status-error'
    return isDragActive ? 'border-brand bg-brand/10' : 'border-white/20'
  }, [status, isDragActive])

  return (
    <div className="w-full">
      <h2 className="text-3xl font-semibold text-center mb-6">{title}</h2>
      <div {...getRootProps()} className={`bg-bg-card rounded-xl p-16 border-2 border-dashed text-center cursor-pointer transition ${borderClass}`}>
        <input {...getInputProps()} />
        <div className="flex flex-col items-center gap-3">
          {status === 'success' ? (
            <CheckCircle className="w-10 h-10 text-status-success" />
          ) : status === 'error' ? (
            <XCircle className="w-10 h-10 text-status-error" />
          ) : (
            <Upload className="w-10 h-10 text-brand" />
          )}
          {status === 'idle' && (
            <>
              <p className="text-textc-secondary">Drag & Drop Files or Click to Browse</p>
              <p className="text-xs text-textc-secondary">Supports: PDF, PNG, JPG</p>
            </>
          )}
          {status === 'uploading' && <p className="text-textc-secondary">Uploading…</p>}
          {status === 'success' && (
            <div className="text-sm">
              <div className="text-textc-primary">{file?.name}</div>
              <button
                type="button"
                className="text-xs underline text-textc-secondary mt-1"
                onClick={(e) => { e.stopPropagation(); setFile(null); setStatus('idle'); onFileSelect(null) }}
              >Remove</button>
            </div>
          )}
          {status === 'error' && <p className="text-status-error text-sm">Invalid file. Max 10MB, PDF/PNG/JPG only.</p>}
        </div>
      </div>
    </div>
  )
}


