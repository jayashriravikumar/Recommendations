import React, { useState } from 'react';
import axios from 'axios';

function StockForecast() {
  const [stockData, setStockData] = useState([]);

  const fetchForecast = async () => {
    try {
      const res = await axios.get('http://localhost:5000/forecast_stock');
      setStockData(res.data);
    } catch (error) {
      console.error("Error fetching forecast", error);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Stock Forecast (Admin View)</h2>
      <button onClick={fetchForecast} className="bg-green-600 text-white px-4 py-2 rounded mb-4">
        Fetch Forecast
      </button>
      <table className="w-full bg-white shadow rounded">
        <thead>
          <tr>
            <th className="p-2">Product ID</th>
            <th className="p-2">Current Stock</th>
            <th className="p-2">Forecasted Demand (7d)</th>
            <th className="p-2">Remaining Stock</th>
            <th className="p-2">Stockout Risk</th>
          </tr>
        </thead>
        <tbody>
          {stockData.map((item) => (
            <tr key={item.pro_id} className="text-center">
              <td className="p-2">{item.pro_id}</td>
              <td className="p-2">{item.current_stock}</td>
              <td className="p-2">{item.forecasted_demand_7d}</td>
              <td className="p-2">{item.remaining_stock}</td>
              <td className={`p-2 font-semibold \${item.stockout_risk ? 'text-red-600' : 'text-green-600'}`}>
                {item.stockout_risk ? 'Yes' : 'No'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default StockForecast;
