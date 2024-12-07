import React from 'react';
import { ChevronRight } from 'lucide-react';
import Logo from '../logo.png'
import { Link } from 'react-router-dom';


const MinervaLanding = () => {
  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-white to-purple-50 relative overflow-hidden">
      <nav className="flex items-center justify-between p-6 md:px-12 lg:px-16">
        <div className="flex items-center space-x-12">
          <span className="text-2xl font-bold text-gray-900">Minerva</span>
          <div className="hidden md:flex space-x-8">
            <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors">About</a>
            <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors">Mission</a>
            <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors">Solutions</a>
            <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors">Our Team</a>
            <a href="#" className="text-gray-700 hover:text-gray-900 transition-colors">Pricing</a>
          </div>
        </div>
        <button className="inline-flex items-center justify-center space-x-2 bg-gray-900 hover:bg-gray-800 text-white px-6 py-2.5 rounded-full transition-colors">
          <span>Sign In</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </nav>
      <main className="container mx-auto px-6 md:px-12 mt-24 md:mt-32 relative z-10">
        <div className="max-w-2xl">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gray-900">Hey Minerva,</h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-12">
            The solution to answer-driven AI in education
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 items-stretch sm:items-center">
            <div className="relative flex-grow max-w-xl">
              <input 
                type="email" 
                placeholder="Email address"
                className="w-full px-6 py-3 bg-gray-100 rounded-full text-gray-800 outline-none focus:ring-2 focus:ring-gray-300 transition-shadow"
              />
            </div>
            <Link to={'http://127.0.0.1:5000/auth/authorize'}>
                <button className="inline-flex items-center justify-center space-x-2 bg-gray-900 hover:bg-gray-800 text-white px-8 py-3 rounded-full transition-colors whitespace-nowrap">
                <span>Start Now</span>
                <ChevronRight className="w-4 h-4" />
                </button>
            </Link>
          </div>
        </div>
      </main>
      <div className="absolute top-1/4 right-0 md:right-16 pointer-events-none">
        <img 
          src={Logo}
          alt="Decorative feather"
          className="w-64 md:w-96"
        />
      </div>
    </div>
  );
};

export default MinervaLanding;