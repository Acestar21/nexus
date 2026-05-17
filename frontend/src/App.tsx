import { useEffect } from "react";
import { useDashboard } from "./hooks/useDashboard";
import { MetricCard } from "./components/MetricCard";
import { Brief } from "./components/Brief";
import { QuickActions } from "./components/QuickActions";

function App() {
  const { data, loading, error, refresh } = useDashboard();

  useEffect(() => {
    refresh();
  }, [refresh]);

  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="app">
      <header className="header">
        <span className="header-title">NEXUS</span>
        <span className="header-date">{today}</span>
      </header>

      {error && <div className="error-banner">ERROR: {error}</div>}

      {loading && !data && (
        <div className="loading">LOADING DASHBOARD...</div>
      )}

      {data && (
        <main className="dashboard">
          <div className="dashboard-left">
            <Brief text={data.brief} />
            <QuickActions onRefresh={refresh} loading={loading} />
          </div>

          <div className="dashboard-right">
            <div className="metrics-grid">
              <MetricCard
                label="GH COMMITS TODAY"
                value={data.github.activity.commits_today}
                sub={`${data.github.activity.commits_this_week} this week`}
              />
              <MetricCard
                label="GH STREAK"
                value={`${data.github.activity.current_streak}d`}
                sub={`last: ${data.github.activity.last_commit_date ?? "—"}`}
                accent={data.github.activity.current_streak > 0}
              />
              <MetricCard
                label="WORKOUT TODAY"
                value={data.fitness.worked_out_today ? "DONE" : "PENDING"}
                sub={`${data.fitness.total_workouts_this_week} this week`}
                accent={data.fitness.worked_out_today}
              />
              <MetricCard
                label="FITNESS STREAK"
                value={`${data.fitness.current_streak}d`}
                sub={`last: ${data.fitness.last_workout_date ?? "—"}`}
                accent={data.fitness.current_streak > 0}
              />
            </div>
            <div className="section-label" style={{ marginTop: "16px" }}>// LEETCODE</div>
            <div className="metrics-grid">
              <MetricCard
                label="LC TODAY"
                value={data.leetcode.activity.problem_solved_today}
                sub={`${data.leetcode.activity.problem_solved_this_week} this week`}
                accent={data.leetcode.activity.problem_solved_today > 0}
              />
              <MetricCard
                label="LC STREAK"
                value={`${data.leetcode.activity.current_streak}d`}
                sub={`max: ${data.leetcode.activity.max_streak}d`}
                accent={data.leetcode.activity.current_streak > 0}
              />
              <MetricCard
                label="TOTAL SOLVED"
                value={data.leetcode.activity.total_problem_solved}
                sub={`${data.leetcode.activity.total_active_days} active days`}
              />
              <MetricCard
                label="LC THIS WEEK"
                value={data.leetcode.activity.problem_solved_this_week}
                sub="problems"
                accent={data.leetcode.activity.problem_solved_this_week > 0}
              />
            </div>
          </div>
        </main>
      )}
    </div>
  );
}

export default App;