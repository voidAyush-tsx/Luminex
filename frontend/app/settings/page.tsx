"use client"
import React from 'react'
import { useApp } from '../../components/AppContext'
import { Card, CardBody, CardTitle } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'

export default function SettingsPage() {
  const { apiBaseUrl, setApiBaseUrl } = useApp()
  return (
    <div className="space-y-8">
      <h1 className="text-4xl md:text-5xl font-semibold">Settings</h1>
      <Card>
        <CardBody>
          <CardTitle>Backend API</CardTitle>
          <div className="mt-4 flex gap-3 items-center">
            <input
              value={apiBaseUrl}
              onChange={(e) => setApiBaseUrl(e.target.value)}
              className="bg-bg-secondary rounded px-3 py-2 w-full"
            />
            <Button onClick={() => {}}>Save</Button>
          </div>
        </CardBody>
      </Card>
    </div>
  )
}


