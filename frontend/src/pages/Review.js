import React, { useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { Home, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Review = () => {
  const [reviewData, setReviewData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [query, setQuery] = useState('');
  const location = useLocation();
  const navigate = useNavigate();
  const selectedCourse = location.state?.selectedCourse;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:5000/ai/generate_review', {
        subject: selectedCourse.name.toLowerCase(),
        storage_path: `${selectedCourse.name.toLowerCase().replace(/\s/g, '_')}_db`,
        query: query.trim()
      });
      setReviewData(response.data);
    } catch (error) {
      console.error('Error fetching review:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Fixed Header */}
      <div className="bg-white shadow-sm px-6 py-4 flex items-center">
        <button
          onClick={() => navigate('/home')}
          className="p-2 hover:bg-gray-100 rounded-full"
        >
          <Home className="w-5 h-5" />
        </button>
        <h1 className="text-xl font-semibold ml-4">{selectedCourse?.name} Review</h1>
      </div>

      {/* Content Container */}
      <div className="flex-1 flex flex-col">
        {/* Search Input - Centered when no content */}
        <div className={`w-full ${!reviewData ? 'flex-1 flex items-center justify-center' : 'bg-gray-50 border-b'}`}>
          <div className="max-w-2xl w-full mx-auto p-6">
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="What would you like to review?"
                className="flex-1 px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-[#9E72C3] focus:border-[#9E72C3]"
                disabled={loading}
              />
              <button
              type="submit"
              className="bg-[#9E72C3] text-white px-4 py-2 rounded-md hover:bg-purple-700 transition-colors duration-200 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              <span>{loading ? 'Loading...' : 'Generate Review'}</span>
              {!loading && <ArrowRight size={20} />}
            </button>
            </form>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex-1 flex justify-center items-center">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#9E72C3] mx-auto"></div>
              <p className="mt-4 text-gray-600">Generating your notes...</p>
            </div>
          </div>
        )}

        {/* Notes Content */}
        {!loading && reviewData && (
          <div className="flex-1 overflow-y-auto">
            <div className="max-w-4xl mx-auto p-6">
              <h1 className="text-3xl font-bold mb-4">{reviewData.title}</h1>
              <p className="text-gray-600 mb-8">{reviewData.introduction}</p>

              {reviewData.sections.map((section, index) => (
                <div key={index} className="mb-10">
                  <h2 className="text-2xl font-semibold mb-4">{section.title}</h2>
                  <p className="text-gray-700 mb-6">{section.content}</p>

                  <div className="mb-6">
                    <h3 className="text-lg font-semibold mb-3">Key Points</h3>
                    <ul className="list-disc pl-6 space-y-2">
                      {section.key_points.map((point, idx) => (
                        <li key={idx} className="text-gray-700">{point}</li>
                      ))}
                    </ul>
                  </div>

                  {section.table && (
                    <div className="overflow-x-auto">
                      <table className="min-w-full border-collapse border border-gray-200">
                        <thead>
                          <tr>
                            {section.table.headers.map((header, idx) => (
                              <th key={idx} className="border border-gray-200 bg-gray-50 px-4 py-2">
                                {header}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {section.table.rows.map((row, rowIdx) => (
                            <tr key={rowIdx}>
                              {row.map((cell, cellIdx) => (
                                <td key={cellIdx} className="border border-gray-200 px-4 py-2">
                                  {cell}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              ))}

              <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                <h3 className="text-lg font-semibold mb-2">Summary</h3>
                <p className="text-gray-700">{reviewData.summary}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Review;