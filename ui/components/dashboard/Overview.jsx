import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { InfoIcon } from "lucide-react";

export default function Overview({ indexData }) {
  const stats = [
    { label: "Ticker", value: "ELEV8" },
    { label: "Exchange", value: "Nasdaq" },
    { label: "Expense Ratio", value: indexData?.expense_ratio + "%" },
    { label: "AUM", value: "$" + (indexData?.aum / 1000000).toFixed(2) + "M" },
    { label: "Management", value: "Smart-Beta" },
  ];

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold mb-4">ELEV8 Index Overview</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-start gap-4">
              <div className="p-3 bg-blue-100 rounded-lg">
                <InfoIcon className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold mb-2">Mission & Philosophy</h3>
                <p className="text-gray-600">
                  ELEV8 Index tracks the performance of top hedge fund holdings, providing investors with institutional-grade investment strategies through a transparent, liquid index vehicle.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="grid grid-cols-2 gap-4">
              {stats.map((stat, i) => (
                <div key={i} className="space-y-1">
                  <p className="text-sm text-gray-500">{stat.label}</p>
                  <p className="text-lg font-semibold">{stat.value}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}