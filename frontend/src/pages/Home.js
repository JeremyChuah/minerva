import React, { useEffect, useState } from "react";
import axios from "axios";

const Home = () => {
  const [courses, setCourses] = useState(null); // To store fetched courses
  const [loading, setLoading] = useState(true); // Loading state

  useEffect(() => {
    // Fetch courses from the endpoint
    const fetchCourses = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/courses/courses");
        setCourses(response.data);
        setLoading(false); // Stop loading when data is fetched
      } catch (error) {
        console.error("Error fetching courses:", error);
        setLoading(false); // Stop loading on error as well
      }
    };

    fetchCourses();
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {loading ? (
        // Loading Spinner
        <div className="flex items-center justify-center space-x-2">
          <div className="w-4 h-4 rounded-full animate-spin border-2 border-blue-500 border-t-transparent"></div>
          <p>Loading...</p>
        </div>
      ) : (
        // Display Courses and Print Button
        <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-6">
          <h1 className="text-2xl font-semibold mb-4">Courses</h1>
          {courses && courses.courses && courses.courses.length > 0 ? (
            <ul>
              {courses.courses.map((course) => (
                <li key={course.id} className="border-b border-gray-200 py-2">
                  {course.name}
                </li>
              ))}
            </ul>
          ) : (
            <p>No courses available.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Home;
