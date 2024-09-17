'use client'

import dynamic from 'next/dynamic'
import { useState, useEffect } from 'react'

const Dashboard = dynamic(() => import('@/components/dashboard'), { ssr: false })

export default function Home() {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      console.error('Caught error:', event.error);
      setError('An error occurred while rendering the dashboard. Please check the console for more details.');
    };

    window.addEventListener('error', handleError);

    return () => {
      window.removeEventListener('error', handleError);
    };
  }, []);

  if (error) {
    return <div className="p-4 text-red-600">{error}</div>;
  }

  return <Dashboard />;
}