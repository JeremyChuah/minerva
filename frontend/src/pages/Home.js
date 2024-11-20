import React, { useEffect, useState } from "react";
import axios from "axios";
import logo from '../logo.png';

const Layout = () => {
  const [courses, setCourses] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/courses/courses");
        setCourses(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching courses:", error);
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading || !courses) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex h-screen">
      <div className="w-64 bg-gray-100 p-6 flex flex-col">
        <div className="flex items-center justify-start mb-8">
          <div className="flex items-center">
            <img src={logo} alt="Minerva Logo" className="w-12 h-12 object-contain" />
            <h1 className="text-2xl font-bold ml-3 leading-none">Minerva</h1>
          </div>
        </div>

        <nav className="space-y-6 flex-grow">
          <div className="space-y-2">
            <h2 className="text-sm font-semibold text-gray-600 uppercase">Subject</h2>
            {courses.courses.map((course) => (
              <div
                key={course.name}
                onClick={() => setSelectedCourse(course)}
                className="flex items-center px-2 py-1 text-gray-700 hover:bg-gray-200 rounded cursor-pointer"
              >
                <div className={`w-2 h-2 rounded-full ${selectedCourse === course ? 'bg-green-500' : 'bg-red-500'} mr-3`} />
                <span>{course.name}</span>
              </div>
            ))}
          </div>
        </nav>
      </div>

      <div className="flex-1 p-8 flex justify-center items-center">
        {selectedCourse ? (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-center mb-6">{selectedCourse.name}</h2>
            <div className="flex gap-4">
              <button className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                Practice Questions
              </button>
              <button className="px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors">
                Review Sheet
              </button>
              <button className="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors">
                Chatbot
              </button>
            </div>
          </div>
        ) : (
          <div className="text-2xl font-bold text-gray-400">
            Select a course
          </div>
        )}
      </div>
    </div>
  );
};

export default Layout;