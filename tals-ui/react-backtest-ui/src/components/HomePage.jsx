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
        flexDirection={{ xs: 'column', sm: 'row' }}
        alignItems="stretch"
        width="100%"
        height="100%"
        padding="1vh"
      >
        <Box sx={{ width: { xs: '100%', sm: '30%' }, pr: { sm: 1 }, pb: { xs: 1, sm: 0 } }}> 
          <ConfigurationForm onBacktestComplete={handleBacktestComplete} />
        </Box>

        <Box sx={{ width: { xs: '100%', sm: '70%' }, pl: { sm: 1 } }}>
          <IndexGraph configId={configId} refreshTrigger={trigger} />
        </Box>
      </Box>

      {/* Flex container for Analytics + Table */}
      <Box
        display="flex"
        flexDirection={{ xs: 'column', sm: 'row' }}
        alignItems="stretch"
        width="100%"
        height="100%"
        padding="1vh"
      >
        <Box sx={{ width: { xs: '100%', sm: '30%' }, pr: { sm: 1 }, pb: { xs: 1, sm: 0 } }}> 
          <AnalyticsPanel configId={configId} />
        </Box>

        <Box sx={{ width: { xs: '100%', sm: '70%' }, pl: { sm: 1 } }}>
          <QuarterlyHoldings configId={configId} />
        </Box>
      </Box>     

      <ExportButton configId={configId} />
    </div>
  );
}

export default HomePage;
