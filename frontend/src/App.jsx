import React from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./context/AuthContext.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import DailyTasksPage from "./pages/DailyTasksPage.jsx";
import StatsPage from "./pages/StatsPage.jsx";
import LeaderboardPage from "./pages/LeaderboardPage.jsx";
import NavBar from "./components/NavBar.jsx";

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

export default function App() {
  const { user } = useAuth();

  return (
    <div className="app-root">
      <NavBar />
      <main className="app-main">
        <Routes>
          <Route
            path="/"
            element={
              user ? <Navigate to="/tasks" replace /> : <Navigate to="/login" replace />
            }
          />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/tasks"
            element={
              <ProtectedRoute>
                <DailyTasksPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/stats"
            element={
              <ProtectedRoute>
                <StatsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/leaderboard"
            element={
              <ProtectedRoute>
                <LeaderboardPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

