import React, { useState, useEffect } from 'react';
import { Configuration } from '@/entities/all';
import { User } from '@/entities/User';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Save } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { createPageUrl } from "@/utils";

export default function Admin() {
  const navigate = useNavigate();
  const [config, setConfig] = useState({
    hedge_funds_count: 10,
    equities_per_fund: 5,
    selection_type: 'top'
  });

  useEffect(() => {
    checkAdmin();
    loadConfig();
  }, []);

  const checkAdmin = async () => {
    try {
      const user = await User.me();
      if (user.role !== 'admin') {
        navigate(createPageUrl("Dashboard"));
      }
    } catch (error) {
      navigate(createPageUrl("Dashboard"));
    }
  };

  const loadConfig = async () => {
    const configs = await Configuration.list();
    if (configs.length > 0) {
      setConfig(configs[0]);
    }
  };

  const handleSave = async () => {
    const configs = await Configuration.list();
    if (configs.length > 0) {
      await Configuration.update(configs[0].id, config);
    } else {
      await Configuration.create(config);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-8">Index Configuration</h1>
      
      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>Strategy Parameters</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium">Number of Hedge Funds</label>
            <Input
              type="number"
              value={config.hedge_funds_count}
              onChange={(e) => setConfig({...config, hedge_funds_count: parseInt(e.target.value)})}
            />
          </div>
          
          <div className="space-y-2">
            <label className="text-sm font-medium">Equities per Fund</label>
            <Input
              type="number"
              value={config.equities_per_fund}
              onChange={(e) => setConfig({...config, equities_per_fund: parseInt(e.target.value)})}
            />
          </div>
          
          <div className="space-y-2">
            <label className="text-sm font-medium">Selection Type</label>
            <Select
              value={config.selection_type}
              onValueChange={(value) => setConfig({...config, selection_type: value})}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="top">Top Performing</SelectItem>
                <SelectItem value="relative">Relative Metrics</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Button onClick={handleSave} className="w-full">
            <Save className="w-4 h-4 mr-2" />
            Save Configuration
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}