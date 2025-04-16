import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const dummyData = [
  { date: '2024-01', ELEV8: 100, SP500: 100 },
  { date: '2024-02', ELEV8: 105, SP500: 102 },
  { date: '2024-03', ELEV8: 110, SP500: 104 },
  { date: '2024-04', ELEV8: 108, SP500: 103 },
  { date: '2024-05', ELEV8: 115, SP500: 106 },
  { date: '2024-06', ELEV8: 120, SP500: 108 },
];

const timeRanges = ['1M', '3M', '6M', 'YTD', '1Y', '3Y'];

export default function PerformanceChart() {
  const [showSP500, setShowSP500] = useState(false);
  const [selectedRange, setSelectedRange] = useState('6M');

  return (
    <Card className="mb-8">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Performance</CardTitle>
        <div className="flex items-center gap-4">
          <div className="flex gap-2">
            {timeRanges.map((range) => (
              <Button
                key={range}
                variant={selectedRange === range ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedRange(range)}
              >
                {range}
              </Button>
            ))}
          </div>
          <Button
            variant={showSP500 ? "default" : "outline"}
            size="sm"
            onClick={() => setShowSP500(!showSP500)}
          >
            Compare S&P 500
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={dummyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="ELEV8"
                stroke="#2563eb"
                fill="#3b82f6"
                fillOpacity={0.1}
                name="ELEV8 Index"
              />
              {showSP500 && (
                <Area
                  type="monotone"
                  dataKey="SP500"
                  stroke="#dc2626"
                  fill="#ef4444"
                  fillOpacity={0.1}
                  name="S&P 500"
                />
              )}
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}