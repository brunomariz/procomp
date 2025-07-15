"use client";

import React, { useState } from "react";
import { WebsiteAnalysisResponse } from "@/types/types";

type Props = {
  onAnalysisStart: () => void;
  onAnalysisComplete: (data: WebsiteAnalysisResponse) => void; // Changed from CompanyProfile
  isLoading: boolean;
};

const URLInput = ({
  onAnalysisStart,
  onAnalysisComplete,
  isLoading,
}: Props) => {
  const [error, setError] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onAnalysisStart();
    setError("");

    const formData = new FormData(e.currentTarget);
    const url = formData.get("url") as string;

    if (!url) {
      setError("Please enter a URL");
      return;
    }

    try {
      console.log("Sending URL to backend:", url);

      const backendUrl =
        process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
      const response = await fetch(`${backendUrl}/api/analyze-website`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Backend response:", data);

      // Pass the full response (WebsiteAnalysisResponse)
      onAnalysisComplete(data);
    } catch (err) {
      console.error("Error analyzing website:", err);
      setError("Failed to analyze website. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-4">
      <div>
        <label
          htmlFor="url"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Company Website URL
        </label>
        <input
          type="url"
          id="url"
          name="url"
          placeholder="https://example.com"
          disabled={isLoading}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
      </div>

      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed"
      >
        {isLoading ? "Analyzing..." : "Generate Profile"}
      </button>
    </form>
  );
};

export default URLInput;
