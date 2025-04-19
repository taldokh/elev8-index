import { useState } from 'react';
import axios from 'axios';

export default function ConfigurationForm({ onBacktestComplete }) {
  const [form, setForm] = useState({
    equities_per_firm: 4,
    number_of_firms: 3,
    selection_type_top: true,
    relative_weight: false,
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
    await axios.post('http://localhost:8000/run-backtest', form);
    onBacktestComplete();
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Configuration</h2>
      <label>
        Equities per Firm:
        <input type="number" name="equities_per_firm" value={form.equities_per_firm} onChange={handleChange} />
      </label>
      <label>
        Number of Firms:
        <input type="number" name="number_of_firms" value={form.number_of_firms} onChange={handleChange} />
      </label>
      <label>
        Selection Type Top:
        <input type="checkbox" name="selection_type_top" checked={form.selection_type_top} onChange={handleChange} />
      </label>
      <label>
        Relative Weight:
        <input type="checkbox" name="relative_weight" checked={form.relative_weight} onChange={handleChange} />
      </label>
      <button type="submit">Run Backtest</button>
    </form>
  );
}
