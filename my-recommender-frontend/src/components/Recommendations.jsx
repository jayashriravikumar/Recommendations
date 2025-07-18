import React, { useState } from 'react';
import axios from 'axios';

function Recommendations() {
  const [userId, setUserId] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const fetchRecommendations = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/recommend?user_id=${userId}`);
      setRecommendations(res.data.recommendations);
    } catch (error) {
      console.error("Error fetching recommendations", error);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <h2 className="text-xl font-bold mb-4">User Recommendations</h2>
      <input
        type="number"
        placeholder="Enter User ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        className="border p-2 rounded mr-2"
      />
      <button onClick={fetchRecommendations} className="bg-blue-600 text-white px-4 py-2 rounded">
        Get Recommendations
      </button>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        {recommendations.map((rec) => (
          <div key={rec.product_id} className="p-4 bg-white rounded shadow">
            <h3 className="font-semibold">{rec.title}</h3>
            <p className="text-sm text-gray-500">Category: {rec.category}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Recommendations;
