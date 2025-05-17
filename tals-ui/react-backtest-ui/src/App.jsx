import { useState } from 'react';
import ConfigurationForm from './components/ConfigurationForm';
import IndexGraph from './components/IndexGraph';
import './App.css';
import logo from './assets/Elev8.png';

function ToggleSection({ title, children }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="info-section">
      <div className="section-header" onClick={() => setExpanded((prev) => !prev)}>
        <h2>{title}</h2>
        <span className="toggle">{expanded ? '−' : '+'}</span>
      </div>
      {expanded && <div className="section-content">{children}</div>}
    </div>
  );
}

function App() {
  const [configId, setConfigId] = useState(null);
  const [trigger, setTrigger] = useState(false);

  const handleBacktestComplete = (newConfigId) => {
    setConfigId(newConfigId);
    setTrigger((prev) => !prev);
  };

  return (
    <div className="container">
      {/* ✅ LOGO SECTION */}
      <div className="header">
        <img src={logo} alt="Logo" />
        <h1>wowowow</h1>
      </div>

      <ConfigurationForm onBacktestComplete={handleBacktestComplete} />
      <IndexGraph configId={configId} refreshTrigger={trigger} />

      {/* 🧠 INFO SECTIONS */}
      <ToggleSection title="Why Elev8?">
        <p>
          Elev8 is designed to capture the collective wisdom of the most successful investment firms.
          By tracking the top holdings of elite hedge funds through their 13F filings, we construct
          an index that mirrors the behavior of institutional giants. This approach offers everyday
          investors a data-driven, research-backed strategy that aligns with the decisions of the
          world's most informed capital allocators.
        </p>
      </ToggleSection>

      <ToggleSection title="Description">
        <p>
          The Elev8 Index is rebalanced quarterly using the most recent 13F filings. We analyze the
          top equity positions from leading hedge funds, filtering for the most significant holdings
          to create a diversified yet targeted index. Our goal is to provide a transparent, rules-based
          strategy that offers exposure to stocks selected by high-conviction institutional investors.
        </p>
      </ToggleSection>

      <ToggleSection title="Allocation Strategy">
      <div className="info-section">
  <div className="section-header">
    <h2>Allocation Strategy</h2>
  </div>
  <div className="section-content">
    <p>
      Our index construction begins with <strong>13F filings</strong>, offering a quarterly snapshot of institutional holdings. 
      Using these disclosures, users define the number of firms and the number of equities per firm to include in the index.
    </p>

    <p>
      The <strong>Selection Type</strong> parameter controls how stocks are chosen:
      <ul>
        <li>
          <strong>Top:</strong> Selects the highest-weighted equities in each firm's portfolio.
        </li>
        <li>
          <strong>Tercile:</strong> Picks stocks evenly across the distribution. For example, if choosing 3 from 9, it selects the 1st, 4th, and 7th by portfolio weight.
        </li>
      </ul>
    </p>

    <p>
      Finally, the <strong>Weighting Method</strong> determines how much each stock contributes to the index:
      <ul>
        <li>
          <strong>Relative Weight:</strong> Stocks are weighted based on their actual portfolio percentage within their firm.
        </li>
        <li>
          <strong>Equal Weight:</strong> All selected equities from a firm share equal weight.
        </li>
      </ul>
    </p>

    <p>
      Regardless of selection or weighting strategy, each firm's contribution to the index remains evenly balanced.
    </p>
  </div>
</div>
      </ToggleSection>
    </div>
  );
}

export default App;
