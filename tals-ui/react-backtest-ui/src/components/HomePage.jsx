import { useState } from 'react';
import ConfigurationForm from './ConfigurationForm';
import IndexGraph from './IndexGraph';
import QuarterlyHoldings from './QuarterlyHoldings';
import AnalyticsPanel from './AnalyticsPanel';
import ExportButton from './ExportButton';
import '../App.css'; // assumes .main-container styles here
import { Box } from '@mui/material';

function HomePage() {
  const [configId, setConfigId] = useState(null);
  const [trigger, setTrigger] = useState(false);

  const handleBacktestComplete = (newConfigId) => {
    setConfigId(newConfigId);
    setTrigger(prev => !prev);
  };

  return (
    <div className="main-container">
      {/* Flex container for Config + Graph */}
      <Box
        display="flex"
        alignItems="stretch"
        width="100%"       // fill the entire parent width
        height="100%"     // or whatever fixed height you want
        padding="1vh"
      >
        <Box sx={{ width: '30%', pr: 1 }}> 
          <ConfigurationForm onBacktestComplete={handleBacktestComplete} />
        </Box>

        <Box sx={{ width: '70%', pl: 1 }}>
          <IndexGraph configId={configId} refreshTrigger={trigger} />
        </Box>
      </Box>

      <Box
        display="flex"
        alignItems="stretch"
        width="100%"       // fill the entire parent width
        height="100%"     // or whatever fixed height you want
        padding="1vh"
      >
        <Box sx={{ width: '30%', pr: 1 }}> 
          <AnalyticsPanel configId={configId} />
        </Box>

        {/* Right: Index Graph (70% width) */}
        <Box sx={{ width: '70%', pl: 1 }}>
          <QuarterlyHoldings configId={configId} />
        </Box>
      </Box>     
      <ExportButton configId={configId} />
    </div>
  );
}

export default HomePage;
