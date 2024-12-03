import React from 'react';
import { Link } from 'react-router-dom';
import { LinkIcon } from '@heroicons/react/24/outline';

function Login() {

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-6">
        <div className="flex flex-col items-center">
          <div className="w-24 h-24 bg-gray-300 rounded-full flex items-center justify-center">
            <img
              src="https://via.placeholder.com/150"
              alt="Profile"
              className="w-16 h-16"
            />
          </div>
          <h2 className="text-xl font-semibold mt-4">Jane Smith</h2>
          <p className="text-gray-500 mt-1">The University of Texas at Austin</p>
        </div>
        <div className="mt-6">
          <Link
            to={'http://127.0.0.1:5000/auth/authorize'}
            className="flex items-center justify-center w-full bg-green-600 text-white p-3 rounded-lg hover:bg-green-700 transition duration-200"
          >
            <div>
              <LinkIcon className="size-6 text-black-500 mr-2" />
            </div>
            Connect with Classroom
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Login;
