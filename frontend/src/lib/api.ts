const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8002";

// ─── Career Intelligence Types (existing) ───

export interface QueryResponse {
  session_id: string;
  status: string;
  message: string;
}

export interface SessionStatus {
  session_id: string;
  status: string;
  query: string;
  query_type: string;
  companies: string[];
  arena_stats: {
    total_posts: number;
    total_comments: number;
    active_agents: number;
    topics: string[];
  };
  report: Report | null;
  elapsed_seconds: number | null;
  created_at: string | null;
}

export interface Report {
  title: string;
  executive_summary: string;
  sections: ReportSection[];
  key_recommendations: string[];
  risk_factors: string[];
  data_quality_note: string;
  next_steps: string[];
}

export interface ReportSection {
  heading: string;
  content: string;
  confidence: number | null;
  key_insights: string[];
  recommendations: string[];
  caveats: string[];
  source_agents: string[];
}

export interface ArenaPost {
  post_id: number;
  agent_id: string;
  agent_name: string;
  agent_type: string;
  topic: string;
  content: string;
  post_type: string;
  confidence: number | null;
  round_num: number;
  likes: number;
  dislikes: number;
  created_at: string;
  comments: ArenaComment[];
}

export interface ArenaComment {
  comment_id: number;
  post_id: number;
  agent_id: string;
  agent_name: string;
  content: string;
  comment_type: string;
  parent_comment_id: number | null;
  round_num: number;
  likes: number;
  dislikes: number;
  created_at: string;
}

export interface SessionLog {
  time: number;
  msg: string;
}

// ─── Interview Types ───

export interface InterviewPanelist {
  name: string;
  role: string;
  personality: string;
  avatar_color: string;
  eval_dimensions?: string[];
}

export interface InterviewTurn {
  turn_number: number;
  speaker: string;
  speaker_role: string;
  content: string;
  turn_type: string;
}

export interface InterviewPreset {
  name: string;
  description: string;
  panel_size: number;
  difficulty: string;
  max_turns: number;
}

export interface InterviewStartResponse {
  session_id: string;
  panel: InterviewPanelist[];
  config: {
    interview_type: string;
    preset: string;
    role: string;
    company: string;
    difficulty: string;
    panel_size: number;
    max_turns: number;
  };
  opening: InterviewTurn[];
}

export interface InterviewAnswerResponse {
  session_id: string;
  responses: InterviewTurn[];
  state: {
    session_id: string;
    status: string;
    turn_number: number;
    orchestrator?: {
      turn_number: number;
      max_turns: number;
      remaining_turns: number;
      coverage: number;
      coverage_by_dimension: Record<string, number>;
    };
  };
}

export interface InterviewScore {
  dimension: string;
  score: number;
  max_score: number;
  evidence: string;
  feedback: string;
}

export interface InterviewEvaluation {
  session_id: string;
  overall: number;
  dimensions: Record<string, number>;
  by_evaluator: Record<
    string,
    {
      role: string;
      scores: Record<string, InterviewScore>;
      overall_impression: string;
      key_observations: string[];
      recommendation: string;
    }
  >;
  action_items: {
    priority: string;
    area: string;
    recommendation: string;
    practice_tip: string;
  }[];
  summary: string;
}

// ─── Career Intelligence API (existing) ───

export async function submitQuery(
  query: string,
  resumeFile?: File
): Promise<QueryResponse> {
  const formData = new FormData();
  formData.append("query", query);
  if (resumeFile) {
    formData.append("resume", resumeFile);
  }

  const res = await fetch(`${API_BASE}/api/query`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getSession(sessionId: string): Promise<SessionStatus> {
  const res = await fetch(`${API_BASE}/api/session/${sessionId}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getArena(
  sessionId: string
): Promise<{ posts: ArenaPost[]; total: number }> {
  const res = await fetch(`${API_BASE}/api/session/${sessionId}/arena`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getSessionLogs(
  sessionId: string
): Promise<{ logs: SessionLog[]; status: string }> {
  const res = await fetch(`${API_BASE}/api/session/${sessionId}/logs`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function listSessions(): Promise<{
  sessions: {
    session_id: string;
    query: string;
    query_type: string;
    status: string;
    created_at: string;
  }[];
}> {
  const res = await fetch(`${API_BASE}/api/sessions`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function createWebSocket(sessionId: string): WebSocket {
  const wsBase = API_BASE.replace("http", "ws");
  return new WebSocket(`${wsBase}/ws/${sessionId}`);
}

// ─── Interview API ───

export async function getInterviewPresets(): Promise<{
  presets: Record<string, InterviewPreset>;
}> {
  const res = await fetch(`${API_BASE}/api/interview/presets`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function startInterview(params: {
  preset: string;
  role: string;
  company: string;
  difficulty: string;
}): Promise<InterviewStartResponse> {
  const formData = new FormData();
  formData.append("preset", params.preset);
  formData.append("role", params.role);
  formData.append("company", params.company);
  formData.append("difficulty", params.difficulty);

  const res = await fetch(`${API_BASE}/api/interview/start`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function submitInterviewAnswer(
  sessionId: string,
  answer: string
): Promise<InterviewAnswerResponse> {
  const formData = new FormData();
  formData.append("answer", answer);

  const res = await fetch(`${API_BASE}/api/interview/${sessionId}/answer`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function endInterview(sessionId: string): Promise<{
  session_id: string;
  evaluation: InterviewEvaluation;
}> {
  const res = await fetch(`${API_BASE}/api/interview/${sessionId}/end`, {
    method: "POST",
  });

  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getInterviewTranscript(
  sessionId: string
): Promise<{ session_id: string; turns: InterviewTurn[] }> {
  const res = await fetch(`${API_BASE}/api/interview/${sessionId}/transcript`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getInterviewEvaluation(
  sessionId: string
): Promise<InterviewEvaluation> {
  const res = await fetch(`${API_BASE}/api/interview/${sessionId}/evaluation`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function createInterviewWebSocket(sessionId: string): WebSocket {
  const wsBase = API_BASE.replace("http", "ws");
  return new WebSocket(`${wsBase}/ws/interview/${sessionId}`);
}

// ─── Multi-Round V2 Types ───

export interface ScreeningStartResponse {
  session_id: string;
  agent_name: string;
  message: string;
  coverage: Record<string, boolean>;
  is_complete: boolean;
}

export interface ScreeningAnswerResponse {
  message: string;
  coverage: Record<string, boolean>;
  coverage_pct: number;
  is_complete: boolean;
  turn_number: number;
}

export interface CandidateProfile {
  name: string;
  experience_level: string;
  domain: string;
  skills: Record<string, string>;
  projects: { name: string; description: string; technologies: string[]; role: string; impact: string }[];
  personality_traits: string[];
  communication_style: string;
  career_goals: string;
  education: string;
  work_history: { company: string; role: string; duration: string; key_work: string }[];
  notable_claims: string[];
  strengths: string[];
  weaknesses: string[];
  target_role: string;
  target_company: string;
}

export interface RoundConfig {
  round_num: number;
  interviewer_name: string;
  interviewer_role: string;
  round_type: string;
  focus_areas: string[];
  max_questions: number;
  is_final: boolean;
  briefing_notes: string;
}

export interface MultiRoundStartResponse {
  session_id: string;
  panel: InterviewPanelist[];
  round_plan: { rounds: RoundConfig[]; total_rounds: number };
  total_rounds: number;
  candidate_profile?: CandidateProfile;
}

export interface RoundStartResponse {
  round_num: number;
  interviewer_name: string;
  interviewer_role: string;
  round_type: string;
  focus_areas: string[];
  opening_message: string;
  is_final: boolean;
}

export interface RoundAnswerResponse {
  is_round_complete: boolean;
  questions_asked: number;
  responses: {
    speaker: string;
    role: string;
    content: string;
    type: string;
  }[];
}

export interface RoundEndResponse {
  round_num: number;
  questions_asked: number;
  next_round: number | null;
  forum_posts: ForumPostData[];
  is_interview_complete: boolean;
}

export interface ForumPostData {
  agent_name: string;
  agent_role: string;
  content: string;
  post_type: string;
  sentiment: string;
  round_num: number;
  post_id: number | null;
  replies: { agent_name: string; content: string }[];
}

export interface ForumRound {
  round_num: number;
  posts: (ArenaPost & { comments: ArenaComment[] })[];
}

// ─── Multi-Round V2 API ───

export async function startScreening(
  name: string = "",
  resumeFile?: File
): Promise<ScreeningStartResponse> {
  const formData = new FormData();
  formData.append("name", name);
  if (resumeFile) {
    formData.append("resume_file", resumeFile);
  }

  const res = await fetch(`${API_BASE}/api/screening/start`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function submitScreeningAnswer(
  sessionId: string,
  answer: string
): Promise<ScreeningAnswerResponse> {
  const formData = new FormData();
  formData.append("answer", answer);

  const res = await fetch(`${API_BASE}/api/screening/${sessionId}/answer`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function completeScreening(
  sessionId: string,
  company: string = "",
  role: string = "",
  panelSize: number = 3
): Promise<MultiRoundStartResponse> {
  const formData = new FormData();
  formData.append("company", company);
  formData.append("role", role);
  formData.append("panel_size", String(panelSize));

  const res = await fetch(`${API_BASE}/api/screening/${sessionId}/complete`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function startRound(
  sessionId: string,
  roundNum: number
): Promise<RoundStartResponse> {
  const res = await fetch(
    `${API_BASE}/api/interview/${sessionId}/round/${roundNum}/start`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function submitRoundAnswer(
  sessionId: string,
  roundNum: number,
  answer: string
): Promise<RoundAnswerResponse> {
  const formData = new FormData();
  formData.append("answer", answer);

  const res = await fetch(
    `${API_BASE}/api/interview/${sessionId}/round/${roundNum}/answer`,
    { method: "POST", body: formData }
  );
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function endRound(
  sessionId: string,
  roundNum: number
): Promise<RoundEndResponse> {
  const res = await fetch(
    `${API_BASE}/api/interview/${sessionId}/round/${roundNum}/end`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getInterviewForum(
  sessionId: string
): Promise<{ session_id: string; rounds: ForumRound[]; summary: Record<string, unknown> }> {
  const res = await fetch(`${API_BASE}/api/interview/${sessionId}/forum`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function evaluateInterview(
  sessionId: string
): Promise<InterviewEvaluation> {
  const res = await fetch(
    `${API_BASE}/api/interview/${sessionId}/evaluate`,
    { method: "POST" }
  );
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getSkillGapReport(
  sessionId: string,
  company?: string,
  role?: string
): Promise<{
  session_id: string;
  target_company: string;
  target_role: string;
  readiness_pct: number;
  gaps: {
    dimension: string;
    current_score: number;
    required_score: number;
    severity: string;
    gap_description: string;
    improvement_plan: string;
    resources: string[];
  }[];
  top_priorities: {
    area: string;
    action: string;
    expected_improvement: string;
  }[];
  overall_assessment: string;
  scores: Record<string, number>;
}> {
  const params = new URLSearchParams();
  if (company) params.set("company", company);
  if (role) params.set("role", role);
  const qs = params.toString() ? `?${params.toString()}` : "";
  const res = await fetch(
    `${API_BASE}/api/interview/${sessionId}/skill-gap${qs}`
  );
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getInterviewRounds(
  sessionId: string
): Promise<{
  session_id: string;
  status: string;
  current_round: number;
  total_rounds: number;
  rounds: { round_num: number; interviewer: string; role: string; status: string; questions_asked: number }[];
}> {
  const res = await fetch(`${API_BASE}/api/interview/${sessionId}/rounds`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
