import { useState } from "react";
import { useNavigate, Outlet, Link } from "react-router-dom";
import { LogOut, Menu, X } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { MENU_ITEMS } from "../constants/menu";

export default function Layout() {
  const { user, signOut } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate("/login");
  };

  console.log("Current User in Layout:", user?.name);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile Header */}
      <div className="lg:hidden fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-30 px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-900">JuzQR</h1>
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 hover:bg-gray-100 rounded-lg transition"
        >
          {sidebarOpen ? (
            <X className="w-6 h-6" />
          ) : (
            <Menu className="w-6 h-6" />
          )}
        </button>
      </div>

      {/* Backdrop */}
      <div
        className={`fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden transition-opacity ${
          sidebarOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
        onClick={() => setSidebarOpen(false)}
      />

      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-white border-r border-gray-200 z-50 transform transition-transform lg:translate-x-0 ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="h-full flex flex-col">
          <div className="p-6 border-b border-gray-200">
            <h1 className="text-2xl font-bold text-amber-900">Chat Bot</h1>
            <p className="text-sm text-gray-600 mt-1">Chat Management System</p>
          </div>

          <nav className="flex-1 p-4 overflow-y-auto">
            <ul className="space-y-1">
              {MENU_ITEMS.map((item) => {
                const Icon = item.icon;

                return (
                  <li key={item.id}>
                    <Link
                      to={item.path}
                      onClick={() => setSidebarOpen(false)}
                      className="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition hover:bg-gray-100"
                    >
                      <Icon className="w-5 h-5" />
                      <span>{item.label}</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>

          {/* User Info + Logout */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center gap-3 mb-3 px-2">
              <div className="w-10 h-10 bg-amber-100 rounded-full flex items-center justify-center">
                <span className="text-amber-900 font-semibold">
                  {user?.name?.charAt(0)?.toUpperCase() ?? "-"}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user?.name ?? "-"}
                </p>
                <p className="text-xs text-gray-500 capitalize">
                  {user?.role?.replace("_", " ") ?? "-"}
                </p>
              </div>
            </div>

            <button
              onClick={handleSignOut}
              className="w-full flex items-center gap-3 px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition"
            >
              <LogOut className="w-5 h-5" />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 pt-16 lg:pt-0 min-h-screen">
        <div className="p-6 lg:p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
