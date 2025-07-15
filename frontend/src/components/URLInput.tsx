"use client"

import React, { useState } from 'react'

type Props = {}

const URLInput = (props: Props) => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string>('')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    
    const formData = new FormData(e.currentTarget)
    const url = formData.get('url') as string
    
    if (!url) {
      setError('Please enter a URL')
      setIsLoading(false)
      return
    }

    try {
      console.log('Sending URL to backend:', url)
      
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
      const response = await fetch(`${backendUrl}/api/analyze-website`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      console.log('Backend response:', data)
      
      // TODO: Handle the response data (e.g., show results, navigate to results page)
      
    } catch (err) {
      console.error('Error analyzing website:', err)
      setError('Failed to analyze website. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <label htmlFor="url" className="text-lg font-semibold">
        Enter Company URL
      </label>
      <input
        type="url"
        id="url"
        name="url"
        placeholder="https://example.com"
        required
        disabled={isLoading}
        className="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
      />
      {error && (
        <p className="text-red-500 text-sm">{error}</p>
      )}
      <button
        type="submit"
        disabled={isLoading}
        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {isLoading ? 'Analyzing...' : 'Generate Profile'}
      </button>
    </form>
  )
}

export default URLInput