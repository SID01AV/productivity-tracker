import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function NavBar() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => (location.pathname === path ? "nav-link active" : "nav-link");

  return (
    <header className="nav-header">
      <div className="nav-brand">Productivity Tracker</div>
      {user && (
        <nav className="nav-links">
          <Link className={isActive("/tasks")} to="/tasks">
            Daily
          </Link>
          <Link className={isActive("/stats")} to="/stats">
            Stats
          </Link>
          <Link className={isActive("/leaderboard")} to="/leaderboard">
            Leaderboard
          </Link>
          <button className="nav-logout" onClick={logout}>
            Logout
          </button>
        </nav>
      )}
    </header>
  );
}

