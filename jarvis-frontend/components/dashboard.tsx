'use client'

import React, { useState, useEffect, useRef } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Home, Brain, Image, FileText, Database, MessageSquare, Settings } from "lucide-react"

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null)
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')
  const [image, setImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [detectedObjects, setDetectedObjects] = useState<string[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        console.log('Fetching metrics...');
        const res = await fetch('/api/metrics');
        console.log('Metrics response status:', res.status);
        console.log('Metrics response headers:', res.headers);
        if (!res.ok) {
          throw new Error(`Failed to fetch metrics: ${res.status} ${res.statusText}`);
        }
        const data = await res.json();
        console.log('Metrics data:', data);
        setMetrics(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching metrics:', err);
        setError(`Failed to load metrics: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, []);

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      setImage(file)
      setImagePreview(URL.createObjectURL(file))
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      let imageFilename = null
      if (image) {
        const formData = new FormData()
        formData.append('file', image)
        const uploadRes = await fetch('/api/upload_image', {
          method: 'POST',
          body: formData,
          credentials: 'include',
        })
        if (!uploadRes.ok) {
          throw new Error(`Failed to upload image: ${uploadRes.statusText}`)
        }
        const uploadData = await uploadRes.json()
        imageFilename = uploadData.filename
      }

      const res = await fetch('/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ query, image_filename: imageFilename }),
        credentials: 'include',
      })

      const contentType = res.headers.get("content-type");
      if (!res.ok) {
        if (contentType && contentType.indexOf("application/json") !== -1) {
          const errorData = await res.json();
          throw new Error(`Failed to process query: ${res.status} ${res.statusText}, ${JSON.stringify(errorData)}`);
        } else {
          const errorText = await res.text();
          throw new Error(`Failed to process query: ${res.status} ${res.statusText}, Response: ${errorText.substring(0, 200)}...`);
        }
      }

      if (!contentType || contentType.indexOf("application/json") === -1) {
        throw new Error(`Expected JSON response but got ${contentType}, Response: ${(await res.text()).substring(0, 200)}...`);
      }

      const data = await res.json()
      setResponse(data.response)

      const objectsMatch = data.response.match(/Detected objects: (.*?)\./)
      if (objectsMatch) {
        setDetectedObjects(objectsMatch[1].split(', '))
      } else {
        setDetectedObjects([])
      }
    } catch (error: any) {
      console.error('Error:', error)
      setError(`An error occurred while processing your query: ${error.message}`)
      setResponse('')
      setDetectedObjects([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <aside className="w-64 bg-gray-800 p-4">
        <h1 className="text-2xl font-bold mb-8">JARVIS</h1>
        <nav>
          <ul className="space-y-2">
            <li><a href="#" className="flex items-center space-x-2 bg-gray-700 p-2 rounded"><Home className="h-5 w-5" /> <span>Dashboard</span></a></li>
            <li><a href="#" className="flex items-center space-x-2 p-2"><Brain className="h-5 w-5" /> <span>Query JARVIS</span></a></li>
            <li><a href="#" className="flex items-center space-x-2 p-2"><Image className="h-5 w-5" /> <span>Image Analysis</span></a></li>
            <li><a href="#" className="flex items-center space-x-2 p-2"><FileText className="h-5 w-5" /> <span>Knowledge Base</span></a></li>
            <li><a href="#" className="flex items-center space-x-2 p-2"><Database className="h-5 w-5" /> <span>RAG Evaluation</span></a></li>
            <li><a href="#" className="flex items-center space-x-2 p-2"><MessageSquare className="h-5 w-5" /> <span>Chat History</span></a></li>
            <li><a href="#" className="flex items-center space-x-2 p-2"><Settings className="h-5 w-5" /> <span>Settings</span></a></li>
          </ul>
        </nav>
      </aside>

      <main className="flex-1 p-8 overflow-auto">
        <h2 className="text-3xl font-bold mb-6">JARVIS Dashboard</h2>

        {error && (
          <Card className="mb-6 bg-red-900 border-red-700">
            <CardContent className="pt-6">
              <p className="text-red-300">{error}</p>
            </CardContent>
          </Card>
        )}

        {loading ? (
          <Card className="mb-6 bg-gray-800">
            <CardContent className="pt-6">
              <p>Loading...</p>
            </CardContent>
          </Card>
        ) : metrics ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            {Object.entries(metrics).map(([key, value]) => (
              <StatCard key={key} title={key.replace('_', ' ')} value={value as string | number} />
            ))}
          </div>
        ) : (
          <Card className="mb-6 bg-gray-800">
            <CardContent className="pt-6">
              <p>No metrics data available.</p>
            </CardContent>
          </Card>
        )}

        <Card className="mb-6 bg-gray-800">
          <CardHeader>
            <CardTitle>Query JARVIS</CardTitle>
            <CardDescription className="text-gray-400">Ask a question or upload an image for analysis</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <Textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your query here..."
                className="min-h-[100px] bg-gray-700 text-white border-gray-600"
              />
              <div className="flex items-center space-x-2">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  ref={fileInputRef}
                  className="hidden"
                />
                <Button type="button" onClick={() => fileInputRef.current?.click()} variant="outline">
                  Upload Image
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Processing...' : 'Submit Query'}
                </Button>
              </div>
              {imagePreview && (
                <img src={imagePreview} alt="Preview" className="mt-2 max-w-xs rounded-md" />
              )}
            </form>
          </CardContent>
        </Card>

        {response && (
          <Card className="mb-6 bg-gray-800">
            <CardHeader>
              <CardTitle>JARVIS Response</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-start space-x-4">
                <Avatar>
                  <AvatarImage src="/jarvis-avatar.png" alt="JARVIS" />
                  <AvatarFallback>JA</AvatarFallback>
                </Avatar>
                <div className="space-y-2">
                  <p>{response}</p>
                  {detectedObjects.length > 0 && (
                    <div>
                      <h4 className="font-semibold">Detected Objects:</h4>
                      <ul className="list-disc list-inside">
                        {detectedObjects.map((obj, index) => (
                          <li key={index}>{obj}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  )
}

function StatCard({ title, value }: { title: string, value: string | number }) {
  return (
    <Card className="bg-gray-800">
      <CardHeader>
        <CardTitle className="capitalize text-gray-300">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-4xl font-bold">
          {typeof value === 'number' ? value.toFixed(2) : value}
          {title.includes('percent') ? '%' : title === 'uptime' ? ' seconds' : ''}
        </div>
      </CardContent>
    </Card>
  )
}