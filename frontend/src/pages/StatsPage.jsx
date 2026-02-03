import React, { useEffect, useState } from "react";
import api from "../api.js";

const RANGES = ["daily", "weekly", "monthly"];

export default function StatsPage() {
  const [range, setRange] = useState("weekly");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadStats = async (r) => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/api/stats/summary", {
        params: { range: r },
      });
      setSummary(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load stats");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats(range);
  }, [range]);

  return (
    <div className="screen">
      <h1 className="screen-title">Your stats</h1>

      <div className="segmented-control">
        {RANGES.map((r) => (
          <button
            key={r}
            className={r === range ? "segment active" : "segment"}
            onClick={() => setRange(r)}
          >
            {r.charAt(0).toUpperCase() + r.slice(1)}
          </button>
        ))}
      </div>

      {loading && <div className="info-text">Loading...</div>}
      {error && <div className="form-error">{error}</div>}

      {summary && !loading && (
        <div className="card stats-card">
          <p className="stats-range">
            {summary.start_date} → {summary.end_date}
          </p>
          <p className="stats-total">
            Total points: <strong>{summary.total_points}</strong>
          </p>

          <h2 className="stats-subtitle">Points by day</h2>
          <ul className="stats-list">
            {summary.by_date.map((d) => (
              <li key={d.date} className="stats-item">
                <span>{d.date}</span>
                <span>{d.points} pts</span>
              </li>
            ))}
            {summary.by_date.length === 0 && (
              <li className="stats-item muted">
                No activity yet in this range.
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

