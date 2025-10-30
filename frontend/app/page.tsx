"use client"
import React, { useState } from 'react'
import UploadForm from '../components/UploadForm'
import Results from '../components/Results'

export default function Page() {
  const [result, setResult] = useState<any | null>(null)
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Upload Invoice & Purchase Order</h1>
        <p className="text-sm text-gray-600">Files are processed by Shivaay AI for extraction and comparison.</p>
      </div>
      <UploadForm onResult={setResult} />
      <Results data={result} />
    </div>
  )
}


