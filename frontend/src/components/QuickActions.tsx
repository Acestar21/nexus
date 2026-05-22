interface QuickActionsProps {
  onRefresh: () => void;
  onRefreshBrief: () => void;
  loading: boolean;
}

export function QuickActions({ onRefresh, onRefreshBrief, loading }: QuickActionsProps) {
  const today = new Date().toISOString().split("T")[0];

  const logWorkout = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/dashboard/log-workout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date: today, completed: true }),
      });
      if (!res.ok) throw new Error("Failed to log workout");
      await onRefresh();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="quick-actions">
      <span className="brief-label">// QUICK ACTIONS</span>
      <div className="actions-row">
        <button className="action-btn" onClick={logWorkout}>
          LOG WORKOUT
        </button>
        <button className="action-btn" onClick={onRefreshBrief} disabled={loading}>
          REFRESH BRIEF
        </button>
        <button 
          className="action-btn action-btn--secondary" 
          onClick={onRefresh} 
          disabled={loading}
        >
          {loading ? "⟳ REFRESHING..." : "REFRESH DATA"}
        </button>
      </div>
    </div>
  );
}