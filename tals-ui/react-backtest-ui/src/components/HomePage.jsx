import { useState } from 'react';
import ConfigurationForm from './ConfigurationForm';
import IndexGraph from './IndexGraph';
import QuarterlyHoldings from './QuarterlyHoldings';
import AnalyticsPanel from './AnalyticsPanel';
import ExportButton from './ExportButton';
import About from './About';

function HomePage() {
  const [configId, setConfigId] = useState(null);
  const [trigger, setTrigger] = useState(false);

  const handleBacktestComplete = (newConfigId) => {
    setConfigId(newConfigId);
    setTrigger(prev => !prev);
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Backtesting</h1>
      </div>

      <ConfigurationForm onBacktestComplete={handleBacktestComplete} />
      <IndexGraph configId={configId} refreshTrigger={trigger} />

      <div className="results-section">
        <div className="results-header">
          <h2>Results</h2>
          <ExportButton configId={configId} />
        </div>
        <QuarterlyHoldings configId={configId} />
        <AnalyticsPanel configId={configId} />
      </div>
    </div>
  );
}

export default HomePage;
