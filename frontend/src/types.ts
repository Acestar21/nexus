export interface CommitActivity {
  commits_today: number;
  commits_this_week: number;
  current_streak: number;
  last_commit_date: string | null;
}

export interface GitHubData {
  username: string;
  captured_at: string;
  activity: CommitActivity;
}

export interface FitnessData {
  captured_at: string;
  worked_out_today: boolean;
  current_streak: number;
  total_workouts_this_week: number;
  last_workout_date: string | null;
}

export interface DashboardData {
  github: GitHubData;
  fitness: FitnessData;
  brief: string;
}

export interface LeetCodeActivity {
  problem_solved_today: number;
  problem_solved_this_week: number;
  total_problem_solved: number;
  current_streak: number;
  max_streak: number;
  total_active_days: number;
}

export interface LeetCodeData {
  username: string;
  captured_at: string;
  activity: LeetCodeActivity;
}

export interface DashboardData {
  github: GitHubData;
  fitness: FitnessData;
  leetcode: LeetCodeData;
  brief: string;
}