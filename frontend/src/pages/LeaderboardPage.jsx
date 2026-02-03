import React, { useEffect, useState } from "react";
import api from "../api.js";

const RANGES = ["daily", "weekly", "monthly"];

export default function LeaderboardPage() {
  const [range, setRange] = useState("weekly");
  const [entries, setEntries] = useState([]);
  const [friends, setFriends] = useState([]);
  const [friendUsername, setFriendUsername] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [friendError, setFriendError] = useState("");

  const loadLeaderboard = async (r) => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/api/leaderboard", {
        params: { range: r },
      });
      setEntries(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load leaderboard");
    } finally {
      setLoading(false);
    }
  };

  const loadFriends = async () => {
    try {
      const res = await api.get("/api/friends");
      setFriends(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadLeaderboard(range);
    loadFriends();
  }, [range]);

  const handleAddFriend = async (e) => {
    e.preventDefault();
    setFriendError("");
    if (!friendUsername.trim()) return;
    try {
      await api.post("/api/friends", {
        friend_username: friendUsername.trim(),
      });
      setFriendUsername("");
      await loadFriends();
    } catch (err) {
      console.error(err);
      setFriendError(err.response?.data?.detail || "Failed to add friend");
    }
  };

  return (
    <div className="screen">
      <h1 className="screen-title">Leaderboard</h1>

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

      <div className="card leaderboard-card">
        <h2 className="card-title">Friends ranking</h2>
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>#</th>
              <th>User</th>
              <th>Points</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((e, idx) => (
              <tr key={e.user_id}>
                <td>{idx + 1}</td>
                <td>{e.username}</td>
                <td>{e.total_points}</td>
              </tr>
            ))}
            {!loading && entries.length === 0 && (
              <tr>
                <td colSpan={3} className="muted">
                  No data yet. Complete some tasks!
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="card friends-card">
        <h2 className="card-title">Your friends</h2>
        <ul className="friends-list">
          {friends.map((f) => (
            <li key={f.id}>
              <span>{f.friend.username}</span>
            </li>
          ))}
          {friends.length === 0 && (
            <li className="muted">No friends yet. Add someone!</li>
          )}
        </ul>

        <form className="form inline-form" onSubmit={handleAddFriend}>
          <input
            className="form-input"
            placeholder="Friend username"
            value={friendUsername}
            onChange={(e) => setFriendUsername(e.target.value)}
          />
          <button className="btn secondary" type="submit">
            Add
          </button>
        </form>
        {friendError && <div className="form-error">{friendError}</div>}
      </div>
    </div>
  );
}

