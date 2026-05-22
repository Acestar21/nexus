import { useEffect, useState } from "react";
import { useDashboard } from "./hooks/useDashboard";
import { MetricCard } from "./components/MetricCard";
import { Brief } from "./components/Brief";
import { QuickActions } from "./components/QuickActions";
import { QuickLinks } from "./components/QuickLinks";
import { ProviderStatus } from "./components/ProviderStatus";

function App() {
  const { data, loading, error, refresh, refreshBrief } = useDashboard();
  const [visibleErrors, setVisibleErrors] = useState<Record<string, boolean>>({});

  useEffect(() => {
    if (!data?.errors) return;
    const hasErrors = Object.values(data.errors).some(val => val !== null);
    if (!hasErrors) return;

    const newErrors: Record<string, boolean> = {};
    Object.entries(data.errors).forEach(([key, val]) => {
      if (val) newErrors[key] = true;
    });

    const showTimer = setTimeout(() => setVisibleErrors(newErrors), 0);
    const hideTimer = setTimeout(() => setVisibleErrors({}), 5000);

    return () => {
      clearTimeout(showTimer);
      clearTimeout(hideTimer);
    };
  }, [data?.errors]);

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
          {data.brief && <Brief text={data.brief} />}

          {visibleErrors.github && (
            <div className="error-banner">GITHUB: {data?.errors.github}</div>
          )}

          <div className="metrics-section">
            <span className="section-label">// GITHUB</span>
              <ProviderStatus
                name="GitHub"
                online={data.provider_status.github.online}
                last_fetched={data.provider_status.github.last_fetched}
                error={data.provider_status.github.error}
              />
            {data.github ? (
              <div className="metrics-row">
                <MetricCard
                  label="COMMITS TODAY"
                  value={data.github.activity.commits_today}
                  sub={`${data.github.activity.commits_this_week} this week`}
                />
                <MetricCard
                  label="GH STREAK"
                  value={`${data.github.activity.current_streak}d`}
                  sub={`last: ${data.github.activity.last_commit_date ?? "—"}`}
                  accent={data.github.activity.current_streak > 0}
                />
              </div>
            ) : (
              <div className="section-error">GitHub data unavailable</div>
            )}
          </div>

          <div className="metrics-section">
            <span className="section-label">// LEETCODE</span>
              <ProviderStatus
                name="LeetCode"
                online={data.provider_status.leetcode.online}
                last_fetched={data.provider_status.leetcode.last_fetched}
                error={data.provider_status.leetcode.error}
              />
            {visibleErrors.leetcode && (
              <div className="error-banner">LEETCODE: {data?.errors.leetcode}</div>
            )}
            {data.leetcode ? (
              <div className="metrics-row">
                <MetricCard
                  label="SOLVED TODAY"
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
              </div>
            ) : (
              <div className="section-error">LeetCode data unavailable</div>
            )}
          </div>

          <div className="metrics-section">
            <span className="section-label">// FITNESS</span>
            <ProviderStatus
              name="Fitness"
              online={data.provider_status.fitness.online}
              last_fetched={data.provider_status.fitness.last_fetched}
              error={data.provider_status.fitness.error}
            />
            {visibleErrors.fitness && (
              <div className="error-banner">FITNESS: {data?.errors.fitness}</div>
            )}
            {data.fitness ? (
              <div className="metrics-row">
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
            ) : (
              <div className="section-error">Fitness data unavailable</div>
            )}
          </div>

          <QuickActions onRefresh={refresh} onRefreshBrief={refreshBrief} loading={loading} />
          <QuickLinks/>
        </main>
      )}
    </div>
  );
}

export default App;