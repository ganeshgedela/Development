import { useState } from "react";

export default function Header() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="relative flex items-center justify-between px-6 h-20 bg-white shadow-sm border-b">
      {/* Left: Logo + Brand */}
      <div className="flex items-center gap-3">
        <img
          src="/tracenova-logo.png"
          alt="TraceNova Logo"
          className="h-12 w-auto object-contain"
        />
        <h1 className="text-2xl font-bold text-gray-800 hidden sm:block">TraceNova</h1>
      </div>

      {/* Center: Subtitle */}
      <div className="absolute left-1/2 transform -translate-x-1/2 text-center">
        <h2 className="text-sm md:text-base lg:text-lg text-gray-600 font-medium tracking-wide">
          AI Network Trace Analyzer
        </h2>
      </div>

      {/* Right: Nav links and Profile */}
      <div className="flex items-center gap-6">
        {/* Navigation links (Desktop Only) */}
        <nav className="hidden md:flex items-center gap-6">
          <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Dashboard</a>
          <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Uploads</a>
          <a href="#" className="text-gray-700 hover:text-blue-600 font-medium">Reports</a>
        </nav>

        {/* Profile Dropdown (Fake for now) */}
        <div className="relative">
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="focus:outline-none flex items-center"
          >
            <img
              src="/avatar-placeholder.png"
              alt="User Avatar"
              className="h-10 w-10 rounded-full object-cover border-2 border-blue-600"
            />
          </button>

          {/* Dropdown Menu */}
          {isOpen && (
            <div className="absolute right-0 mt-2 w-40 bg-white border rounded shadow-lg py-2">
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
              <a href="#" className="block px-4 py-2 text-sm text-red-600 hover:bg-gray-100">Logout</a>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
