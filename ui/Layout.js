import React from "react";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import { User } from "@/entities/User";
import { BarChart, Settings, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function Layout({ children, currentPageName }) {
  const [isAdmin, setIsAdmin] = React.useState(false);

  React.useEffect(() => {
    checkAdmin();
  }, []);

  const checkAdmin = async () => {
    try {
      const user = await User.me();
      setIsAdmin(user.role === 'admin');
    } catch (error) {
      setIsAdmin(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <nav className="border-b bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <Link to={createPageUrl("Dashboard")} className="flex items-center">
                <span className="text-2xl font-bold text-blue-600">ELEV8</span>
                <span className="ml-2 text-gray-600">Index</span>
              </Link>
            </div>
            <div className="flex items-center gap-4">
              <Link to={createPageUrl("Dashboard")}>
                <Button variant="ghost" className="gap-2">
                  <BarChart className="w-4 h-4" />
                  Dashboard
                </Button>
              </Link>
              {isAdmin && (
                <Link to={createPageUrl("Admin")}>
                  <Button variant="ghost" className="gap-2">
                    <Settings className="w-4 h-4" />
                    Admin
                  </Button>
                </Link>
              )}
              <Button 
                variant="ghost" 
                className="gap-2"
                onClick={() => User.logout()}
              >
                <LogOut className="w-4 h-4" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}