import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './QuarterlyHoldings.css';

function QuarterlyHoldings({ configId }) {
  const [data, setData] = useState({});
  const [quarters, setQuarters] = useState([]);
  const [selectedQuarter, setSelectedQuarter] = useState('');

  useEffect(() => {
    axios
      .get(import.meta.env.VITE_API_URL + `/equities-by-quarter?config_id=${configId}`)
      .then((res) => {
        setData(res.data);
        const q = Object.keys(res.data).sort(); // ISO strings sort chronologically
        setQuarters(q);
        if (q.length > 0) setSelectedQuarter(q[0]);
      })
      .catch((err) => console.error('Error fetching data:', err));
  }, [configId]);

  return (
    <div className="holdings-container">
      <h2>Equity Holdings</h2>

      {quarters.length > 0 ? (
        <>
          <label>
            Select Quarter:{' '}
            <select
              value={selectedQuarter}
              onChange={(e) => setSelectedQuarter(e.target.value)}
            >
              {quarters.map((q) => (
                <option key={q} value={q}>
                  {q}
                </option>
              ))}
            </select>
          </label>

          <table className="holdings-table">
            <thead>
              <tr>
                <th>Ticker</th>
                <th>Weight (%)</th>
              </tr>
            </thead>
            <tbody>
              {data[selectedQuarter].map((row) => (
                <tr key={row.ticker}>
                  <td>{row.ticker}</td>
                  <td>{row.weight.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      ) : (
        <p>No holdings data found for this configuration.</p>
      )}
    </div>
  );
}

export default QuarterlyHoldings;
