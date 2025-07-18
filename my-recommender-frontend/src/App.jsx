// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './components/HomePage';
import Recommendations from './components/Recommendations';
import StockForecast from './components/StockForecast';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 p-4">
        <nav className="flex justify-center mb-6">
          <Link
            to="/recommend"
            className="mx-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            User Dashboard
          </Link>
          <Link
            to="/stock"
            className="mx-4 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Admin Dashboard
          </Link>
        </nav>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recommend" element={<Recommendations />} />
          <Route path="/stock" element={<StockForecast />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
