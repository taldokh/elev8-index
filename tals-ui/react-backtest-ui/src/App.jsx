import { useState } from 'react';
import ConfigurationForm from './components/ConfigurationForm';
import IndexGraph from './components/IndexGraph';
import './App.css';


function App() {
  const [trigger, setTrigger] = useState(false);

  const handleBacktestComplete = () => {
    setTrigger(prev => !prev); // refresh the chart on toggle
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Backtesting UI</h1>
      <ConfigurationForm onBacktestComplete={handleBacktestComplete} />
      <IndexGraph refreshTrigger={trigger} />
    </div>
  );
}

export default App;
