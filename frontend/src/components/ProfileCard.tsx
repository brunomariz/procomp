import React from "react";
import { WebsiteAnalysisResponse } from "../types/types";

type Props = { data: WebsiteAnalysisResponse };

const ProfileCard = ({ data }: Props) => {
  const {
    url,
    analysis: {
      company_description,
      company_name,
      poc,
      emails,
      tier1_keywords,
      tier2_keywords,
    },
  } = data;

  // Debug log to check emails
  console.log("ProfileCard data:", { emails, poc, company_name });

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden">
      {/* Header Section */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">{company_name}</h1>
            <div className="flex items-center text-blue-100">
              <svg
                className="w-4 h-4 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM4.332 8.027a6.012 6.012 0 011.912-2.706C6.512 5.73 6.974 6 7.5 6A1.5 1.5 0 019 7.5V8a2 2 0 004 0 2 2 0 011.523-1.943A5.977 5.977 0 0116 10c0 .34-.028.675-.083 1H15a2 2 0 00-2 2v2.197A5.973 5.973 0 0110 16v-2a2 2 0 00-2-2 2 2 0 01-2-2 2 2 0 00-1.668-1.973z"
                  clipRule="evenodd"
                />
              </svg>
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-white transition-colors truncate"
              >
                {url}
              </a>
            </div>
          </div>
          <div className="text-right">
            <div className="bg-blue-500 bg-opacity-50 rounded-lg px-3 py-1 text-sm">
              Company Profile
            </div>
          </div>
        </div>
      </div>

      {/* Content Section */}
      <div className="p-6">
        {/* Company Description */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <svg
              className="w-5 h-5 mr-2 text-blue-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clipRule="evenodd"
              />
            </svg>
            About
          </h2>
          <p className="text-gray-600 leading-relaxed bg-gray-50 p-4 rounded-lg">
            {company_description}
          </p>
        </div>

        {/* Contact Information */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <svg
              className="w-5 h-5 mr-2 text-green-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
            </svg>
            Contact Information
          </h2>
          <div className="bg-gray-50 p-4 rounded-lg">
            {poc && (
              <div className="mb-2">
                <span className="font-medium text-gray-700">
                  Point of Contact:
                </span>
                <span className="ml-2 text-gray-600">{poc}</span>
              </div>
            )}
            {emails.length > 0 && (
              <div>
                <span className="font-medium text-gray-700">
                  Email Addresses:
                </span>
                <div className="mt-1 space-y-1">
                  {emails.map((email: string, index: number) => (
                    <div key={index} className="ml-2">
                      <a
                        href={`mailto:${email}`}
                        className="text-blue-600 hover:text-blue-800 transition-colors"
                      >
                        {email}
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {!poc && emails.length === 0 && (
              <p className="text-gray-500 italic">
                No contact information available
              </p>
            )}
          </div>
        </div>

        {/* Keywords Section */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Primary Keywords */}
          <div>
            <h2 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <svg
                className="w-5 h-5 mr-2 text-purple-600"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M9.243 3.03a1 1 0 01.727 1.213L9.53 6h2.94l.56-2.243a1 1 0 111.94.486L14.53 6H17a1 1 0 110 2h-2.97l-1 4H15a1 1 0 110 2h-2.47l-.56 2.242a1 1 0 11-1.94-.485L10.47 14H7.53l-.56 2.242a1 1 0 11-1.94-.485L5.47 14H3a1 1 0 110-2h2.97l1-4H5a1 1 0 110-2h2.47l.56-2.243a1 1 0 011.213-.727zM9.03 8l-1 4h2.94l1-4H9.03z"
                  clipRule="evenodd"
                />
              </svg>
              Primary Keywords
            </h2>
            <div className="space-y-2">
              {tier1_keywords.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {tier1_keywords.map((keyword: string, index: number) => (
                    <span
                      key={index}
                      className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 italic">
                  No primary keywords found
                </p>
              )}
            </div>
          </div>

          {/* Secondary Keywords */}
          <div>
            <h2 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
              <svg
                className="w-5 h-5 mr-2 text-indigo-600"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M17.707 9.293a1 1 0 010 1.414l-7 7a1 1 0 01-1.414 0l-7-7A.997.997 0 012 10V5a3 3 0 013-3h5c.256 0 .512.098.707.293l7 7zM5 6a1 1 0 100-2 1 1 0 000 2z"
                  clipRule="evenodd"
                />
              </svg>
              Secondary Keywords
            </h2>
            <div className="space-y-2">
              {tier2_keywords.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {tier2_keywords.map((keyword: string, index: number) => (
                    <span
                      key={index}
                      className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500 italic">
                  No secondary keywords found
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
        <div className="flex justify-between items-center text-sm text-gray-500">
          <span>Analysis generated from website content</span>
          <span>{new Date().toLocaleDateString()}</span>
        </div>
      </div>
    </div>
  );
};

export default ProfileCard;
