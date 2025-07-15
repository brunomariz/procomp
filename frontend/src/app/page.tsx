"use client";

import URLInput from "@/components/URLInput";
import ProfileCard from "@/components/ProfileCard";
import { useState } from "react";
import { WebsiteAnalysisResponse } from "@/types/types";

export default function Home() {
  const [analysisData, setAnalysisData] =
    useState<WebsiteAnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalysisComplete = (data: WebsiteAnalysisResponse) => {
    setAnalysisData(data);
    setIsLoading(false);
  };

  const handleAnalysisStart = () => {
    setIsLoading(true);
    setAnalysisData(null);
  };

  return (
    <div className="min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      {!analysisData ? (
        // Show the input form when no data
        <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen">
          <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
            <h1 className="text-4xl font-bold">ProComp</h1>
            <p className="text-lg text-gray-600">Company profile generator</p>
            <div className="w-full max-w-md">
              <URLInput
                onAnalysisStart={handleAnalysisStart}
                onAnalysisComplete={handleAnalysisComplete}
                isLoading={isLoading}
              />
            </div>
          </main>
          <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
            © Copyright 2025, Bruno Mariz
          </footer>
        </div>
      ) : (
        // Show the profile card when data is available
        <div className="container mx-auto">
          {/* Header with back button */}
          <div className="mb-8 flex items-center justify-between">
            <h1 className="text-3xl font-bold">Company Profile</h1>
            <button
              onClick={() => setAnalysisData(null)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Analyze Another Company
            </button>
          </div>

          {/* Profile Card */}
          <ProfileCard data={analysisData} />

          {/* Footer */}
          <footer className="mt-8 text-center text-gray-500">
            © Copyright 2025, Bruno Mariz
          </footer>
        </div>
      )}
    </div>
  );
}
