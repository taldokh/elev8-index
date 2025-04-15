import React, { useEffect, useState } from 'react';
import { IndexData, Holding } from '@/entities/all';
import Overview from '../components/dashboard/Overview.jsx';
import PerformanceChart from '../components/dashboard/PerformanceChart.js';
import Holdings from '../components/dashboard/Holdings.jsx';

export default function Dashboard() {
  const [indexData, setIndexData] = useState(null);
  const [holdings, setHoldings] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const [indexDataList, holdingsList] = await Promise.all([
      IndexData.list(),
      Holding.list()
    ]);
    
    if (indexDataList.length > 0) {
      setIndexData(indexDataList[0]);
    }
    setHoldings(holdingsList);
  };

  return (
    <div>
      <Overview indexData={indexData} />
      <PerformanceChart />
      <Holdings holdings={holdings} />
    </div>
  );
}