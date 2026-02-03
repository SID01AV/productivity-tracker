import React, { useEffect, useState } from "react";
import api from "../api.js";

export default function DailyTasksPage() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchDaily = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/api/tasks/daily");
      setItems(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDaily();
  }, []);

  const toggleTask = async (taskId, currentCompleted, date) => {
    try {
      await api.post("/api/daily-logs", {
        task_id: taskId,
        date,
        completed: !currentCompleted,
      });
      setItems((prev) =>
        prev.map((item) =>
          item.task.id === taskId
            ? {
                ...item,
                completed: !currentCompleted,
                points_awarded: !currentCompleted ? item.task.points : 0,
              }
            : item
        )
      );
    } catch (err) {
      console.error(err);
      setError("Failed to update task");
    }
  };

  const todayLabel = items[0]?.date || new Date().toISOString().slice(0, 10);

  return (
    <div className="screen">
      <h1 className="screen-title">Today&apos;s tasks</h1>
      <p className="screen-subtitle">Date: {todayLabel}</p>

      {loading && <div className="info-text">Loading...</div>}
      {error && <div className="form-error">{error}</div>}

      <div className="card-list">
        {items.map((item) => (
          <div key={item.task.id} className="card task-card">
            <div className="task-main">
              <div>
                <h2 className="task-title">{item.task.name}</h2>
                {item.task.description && (
                  <p className="task-desc">{item.task.description}</p>
                )}
              </div>
              <div className="task-points">+{item.task.points} pts</div>
            </div>
            <div className="task-footer">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={item.completed}
                  onChange={() =>
                    toggleTask(item.task.id, item.completed, item.date)
                  }
                />
                <span>Completed</span>
              </label>
              <div className="task-earned">
                Earned: <strong>{item.points_awarded}</strong> pts
              </div>
            </div>
          </div>
        ))}

        {!loading && items.length === 0 && (
          <div className="info-text">No tasks configured.</div>
        )}
      </div>
    </div>
  );
}

