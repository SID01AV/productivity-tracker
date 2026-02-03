import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function LoginPage() {
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || "/tasks";

  const [mode, setMode] = useState("login"); // 'login' | 'register'
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (mode === "login") {
        await login(username, password);
      } else {
        await register(username, email, password);
      }
      navigate(from, { replace: true });
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="screen screen-center">
      <div className="card auth-card">
        <h1 className="card-title">
          {mode === "login" ? "Welcome back" : "Create an account"}
        </h1>
        <p className="card-subtitle">
          Track your daily habits and compete with friends.
        </p>

        <form className="form" onSubmit={handleSubmit}>
          <label className="form-label">
            Username
            <input
              className="form-input"
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </label>

          {mode === "register" && (
            <label className="form-label">
              Email (optional)
              <input
                className="form-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </label>
          )}

          <label className="form-label">
            Password
            <input
              className="form-input"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>

          {error && <div className="form-error">{error}</div>}

          <button className="btn primary" type="submit" disabled={loading}>
            {loading
              ? "Please wait..."
              : mode === "login"
              ? "Log in"
              : "Register & continue"}
          </button>
        </form>

        <button
          className="link-button"
          type="button"
          onClick={() => {
            setMode(mode === "login" ? "register" : "login");
            setError("");
          }}
        >
          {mode === "login"
            ? "No account yet? Create one"
            : "Already have an account? Log in"}
        </button>
      </div>
    </div>
  );
}

