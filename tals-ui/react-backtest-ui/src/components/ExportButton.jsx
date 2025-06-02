import { useState } from 'react';
import { Fab, CircularProgress, Tooltip } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

function ExportButton({ configId }) {
  const [isLoading, setIsLoading] = useState(false);

  const handleExport = async () => {
    if (!configId) {
      alert('Please run a backtest first');
      return;
    }

    try {
      setIsLoading(true);
      const response = await fetch(import.meta.env.VITE_API_URL + `/export?config_id=${configId}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Export failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `backtest_export_${configId}.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Tooltip title="Export to Excel">
      <span> {/* Tooltip won't show if child is disabled directly, so wrap it */}
        <Fab
          color="success"
          onClick={handleExport}
          disabled={isLoading || !configId}
          sx={{
            position: 'fixed',
            bottom: 24,
            left: 24,
            zIndex: 1000,
          }}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : <DownloadIcon />}
        </Fab>
      </span>
    </Tooltip>
  );
}

export default ExportButton;
