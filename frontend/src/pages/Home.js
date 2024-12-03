import React, { useEffect, useState } from "react";
import axios from "axios";
import logo from '../logo.png';
import { BookOpen } from 'lucide-react';
import { ClipLoader } from "react-spinners"; // Import spinner
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const [courses, setCourses] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [loadingCourseMaterials, setLoadingCourseMaterials] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/courses/courses");
        setCourses(response.data.courses);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching courses:", error);
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const handleCourseSelect = async (course) => {
    try {
      setSelectedCourse(course);
      const response = await axios.post("http://127.0.0.1:5000/courses/get_courses", {
        course_id: course.id,
        subject: course.name.toLowerCase().replace(/\s/g, '_')
      }).then(() => {
        setLoadingCourseMaterials(false);
      })
    } catch (error) {
      console.error("Error fetching course materials:", error);
    }
  };

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
            <h2 className="text-sm font-semibold text-gray-600 uppercase">Courses</h2>
            {courses.map((course) => (
              <div
                key={course.id}
                onClick={() => handleCourseSelect(course)}
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
          loadingCourseMaterials ? (
            <div className="flex flex-col items-center">
              <ClipLoader size={50} color={"#4A90E2"} />
              <div className="text-xl font-bold text-gray-400 mt-4">Loading course materials...</div>
            </div>
          ) : (
            <div className="space-y-4 w-full max-w-md">
              <h2 className="text-2xl font-bold text-center mb-8">{selectedCourse.name}</h2>
              <div className="space-y-4">
                <button
                  className="w-full flex items-center p-6 bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-all group"
                  onClick={() => navigate('/practice-questions', { state: {selectedCourse: selectedCourse}})                }
                >
                  <div className="w-12 h-12 bg-indigo-50 rounded-lg flex items-center justify-center group-hover:bg-indigo-100 transition-colors">
                    <BookOpen className="w-6 h-6 text-indigo-600" />
                  </div>
                  <div className="ml-4 text-left">
                    <h3 className="font-semibold text-gray-900">Practice Questions</h3>
                    <p className="text-sm text-gray-500">Test your knowledge with practice problems</p>
                  </div>
                </button>
              </div>
            </div>
          )
        ) : (
          <div className="text-2xl font-bold text-gray-400">
            Select a course
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;