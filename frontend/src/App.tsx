import React, { useState } from 'react';
import './App.css';

interface AnalysisResult {
  match_percentage: string;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  is_fallback?: boolean;
  fallback_reason?: string;
}

function App() {
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState('');
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Backend API URL - use environment variable in production
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      setCvFile(file);
      setError('');
    } else {
      setError('Please upload a PDF file');
      setCvFile(null);
    }
  };

  const handleAnalyze = async () => {
    if (!cvFile || !jobDescription.trim()) {
      setError('Please upload a CV and provide a job description');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('cv_file', cvFile);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch(`${API_BASE_URL}/api/analyze`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setAnalysis(result);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Failed to connect to the server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getMatchColor = (percentage: string) => {
    const num = parseInt(percentage);
    if (num >= 80) return 'text-green-600';
    if (num >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              CV Matchy-Matchy
            </h1>
            <p className="text-gray-600 text-lg">
              Analyze your CV against job descriptions and get personalized insights
            </p>
          </div>

          {/* Main Form */}
          <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
            <div className="grid md:grid-cols-2 gap-6">
              {/* CV Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload Your CV (PDF)
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileChange}
                    className="hidden"
                    id="cv-upload"
                  />
                  <label htmlFor="cv-upload" className="cursor-pointer">
                    <div className="text-gray-600">
                      <svg className="mx-auto h-12 w-12 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                      </svg>
                      <p className="text-lg font-medium">
                        {cvFile ? cvFile.name : 'Click to upload PDF'}
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        {cvFile ? 'File selected' : 'Drag and drop or click to browse'}
                      </p>
                    </div>
                  </label>
                </div>
              </div>

              {/* Job Description */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Job Description
                </label>
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  placeholder="Paste the job description here..."
                  className="w-full h-48 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {error}
              </div>
            )}

            {/* Analyze Button */}
            <div className="mt-6 text-center">
              <button
                onClick={handleAnalyze}
                disabled={loading || !cvFile || !jobDescription.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
              >
                {loading ? 'Analyzing...' : 'Analyze CV'}
              </button>
            </div>
          </div>

          {/* Analysis Results */}
          {analysis && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
                Analysis Results
              </h2>

              {/* Fallback Indicator */}
              {analysis.is_fallback && (
                <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <div className="flex items-center">
                    <svg className="w-5 h-5 text-yellow-600 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <div>
                      <h3 className="text-sm font-medium text-yellow-800">
                        AI Analysis Unavailable
                      </h3>
                      <p className="text-sm text-yellow-700 mt-1">
                        The AI analysis service is currently unavailable. This is a basic keyword-based analysis.
                        {analysis.fallback_reason && (
                          <span className="block mt-1 text-xs text-yellow-600">
                            Reason: {analysis.fallback_reason}
                          </span>
                        )}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Match Percentage */}
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                  <div className="text-center">
                    <div className={`text-3xl font-bold ${getMatchColor(analysis.match_percentage)}`}>
                      {analysis.match_percentage}%
                    </div>
                    <div className="text-sm opacity-90">Match</div>
                  </div>
                </div>
              </div>

              <div className="grid md:grid-cols-3 gap-6">
                {/* Strengths */}
                <div className="bg-green-50 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-green-800 mb-3 flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    Strengths
                  </h3>
                  <ul className="space-y-2">
                    {analysis.strengths.map((strength, index) => (
                      <li key={index} className="text-green-700 text-sm flex items-start">
                        <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                        {strength}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Weaknesses */}
                <div className="bg-red-50 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-red-800 mb-3 flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                    Areas for Improvement
                  </h3>
                  <ul className="space-y-2">
                    {analysis.weaknesses.map((weakness, index) => (
                      <li key={index} className="text-red-700 text-sm flex items-start">
                        <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                        {weakness}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Suggestions */}
                <div className="bg-blue-50 rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-blue-800 mb-3 flex items-center">
                    <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                    Suggestions
                  </h3>
                  <ul className="space-y-2">
                    {analysis.suggestions.map((suggestion, index) => (
                      <li key={index} className="text-blue-700 text-sm flex items-start">
                        <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App; 