import { useState } from 'react';
import axios from 'axios';

export default function ConfigurationForm({ onBacktestComplete }) {
  const [form, setForm] = useState({
    equities_per_firm: 1,
    number_of_firms: 5,
    selection_type_top: true,
    relative_weight: true,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const params = {
        ...form,
        equities_per_firm: parseInt(form.equities_per_firm),
        number_of_firms: parseInt(form.number_of_firms),
      };
      const existsResponse = await axios.get('http://localhost:8010/conf-exists', { params });
      const { exists, id: configId } = existsResponse.data;

      if (exists) {
        const readyResponse = await axios.get('http://localhost:8010/conf-ready', {
          params: { conf_id: configId },
        });

        if (readyResponse.data.ready) {
          onBacktestComplete(configId); // ✅ tell App it's ready
          return;
        } else {
          alert('Backtest is already running. please try again later');
        }
      } else {
          // If config doesn't exist, trigger the backtest
        await axios.post('http://localhost:8010/run-backtest', params);

        // You could poll for readiness here, or just ask user to retry in a few moments
        alert('Backtest started. Please wait and try again shortly.');
      }
    } catch (error) {
      console.error('Error during backtest submission:', error);
      alert('Something went wrong. Check the console.');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Configuration</h2>
      <label>
        Equities per Firm:
        <input
          type="number"
          name="equities_per_firm"
          value={form.equities_per_firm}
          onChange={handleChange}
        />
      </label>
      <label>
        Number of Firms:
        <input
          type="number"
          name="number_of_firms"
          value={form.number_of_firms}
          onChange={handleChange}
        />
      </label>
      <label>
        Selection Type Top:
        <input
          type="checkbox"
          name="selection_type_top"
          checked={form.selection_type_top}
          onChange={handleChange}
        />
      </label>
      <label>
        Relative Weight:
        <input
          type="checkbox"
          name="relative_weight"
          checked={form.relative_weight}
          onChange={handleChange}
        />
      </label>
      <button type="submit">Run Backtest</button>
    </form>
  );
}
