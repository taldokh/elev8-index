import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { TrendingUp, TrendingDown } from "lucide-react";

export default function Holdings({ holdings }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>Top Holdings</CardTitle>
          <span className="text-sm text-gray-500">
            As of {new Date().toLocaleDateString()}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Company</TableHead>
              <TableHead>Ticker</TableHead>
              <TableHead className="text-right">Weight</TableHead>
              <TableHead className="text-right">Last Price</TableHead>
              <TableHead className="text-right">Daily Change</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {holdings.map((holding) => (
              <TableRow key={holding.ticker}>
                <TableCell className="font-medium">
                  {holding.company_name}
                </TableCell>
                <TableCell>{holding.ticker}</TableCell>
                <TableCell className="text-right">
                  {holding.weight.toFixed(2)}%
                </TableCell>
                <TableCell className="text-right">
                  ${holding.last_price.toFixed(2)}
                </TableCell>
                <TableCell className="text-right">
                  <span className={`flex items-center justify-end gap-1 ${
                    holding.daily_change >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {holding.daily_change >= 0 ? (
                      <TrendingUp className="w-4 h-4" />
                    ) : (
                      <TrendingDown className="w-4 h-4" />
                    )}
                    {Math.abs(holding.daily_change).toFixed(2)}%
                  </span>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  );
}