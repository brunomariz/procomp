import React from "react";

export interface CompanyProfile {
  company_name: string;
  company_description: string;
  tier1_keywords: string[];
  tier2_keywords: string[];
  emails: string[];
  poc: string;
}

export interface WebsiteAnalysisResponse {
  url: string;
  analysis: CompanyProfile;
}
