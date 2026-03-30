"""
InterviewForum — Hidden inter-interviewer discussion between rounds.

After each round, non-active interviewers observe the transcript and post
their thoughts in a hidden forum. This creates the "behind the scenes"
discussion that gets revealed to the candidate at the end — the viral moment.

Uses the existing arena_posts/arena_comments tables via CareerDB.
"""

from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict

from database import CareerDB
from llm_client import LLMClient
from interviewer_personas import InterviewerPersona

logger = logging.getLogger(__name__)


@dataclass
class ForumPost:
    agent_name: str
    agent_role: str
    content: str
    post_type: str = "observation"  # observation, concern, praise, question, strategy
    sentiment: str = "neutral"  # positive, neutral, negative, mixed
    round_num: int = 0
    post_id: Optional[int] = None
    replies: List[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


class InterviewForum:
    def __init__(self, db: CareerDB, llm: LLMClient):
        self.db = db
        self.llm = llm

    def run_observer_round(
        self,
        session_id: str,
        round_num: int,
        active_interviewer: str,
        round_transcript: str,
        panel: List[InterviewerPersona],
        candidate_summary: str = "",
        previous_forum: str = "",
    ) -> List[ForumPost]:
        """
        After Round N: all non-active interviewers observe the transcript
        and post their thoughts. Runs observers in parallel.
        """
        observers = [p for p in panel if p.name != active_interviewer]
        if not observers:
            return []

        forum_posts: List[ForumPost] = []

        with ThreadPoolExecutor(max_workers=len(observers)) as pool:
            futures = {
                pool.submit(
                    self._generate_observation,
                    session_id, round_num, observer,
                    active_interviewer, round_transcript,
                    candidate_summary, previous_forum,
                ): observer
                for observer in observers
            }
            for future in as_completed(futures):
                observer = futures[future]
                try:
                    post = future.result()
                    if post:
                        forum_posts.append(post)
                except Exception as e:
                    logger.error(f"Observer {observer.name} failed: {e}")

        # Generate replies between observers
        if len(forum_posts) >= 2:
            self._generate_replies(session_id, round_num, forum_posts, panel)

        return forum_posts

    def _generate_observation(
        self,
        session_id: str,
        round_num: int,
        observer: InterviewerPersona,
        active_interviewer: str,
        round_transcript: str,
        candidate_summary: str,
        previous_forum: str,
    ) -> Optional[ForumPost]:
        """Generate a single observer's forum post."""
        prompt = f"""You are {observer.name} ({observer.role}), observing Round {round_num} conducted by {active_interviewer}.

You are in a private inter-interviewer forum. The candidate CANNOT see this. Share your honest observations with the other interviewers.

## Your Evaluation Focus
{', '.join(observer.eval_dimensions)}

## Candidate Summary
{candidate_summary or 'No prior data yet.'}

{f'## Previous Forum Discussion{chr(10)}{previous_forum}' if previous_forum else ''}

## Round {round_num} Transcript
{round_transcript}

---

Based on what you observed, write a forum post sharing:
1. Your key observation about the candidate's performance in this round
2. Any strengths or concerns from your area of expertise
3. Specific things you want to probe in YOUR upcoming round (if applicable)
4. Whether you agree/disagree with the interviewer's approach

Keep it conversational and honest — like real interviewers chatting between rounds.
Write 3-5 sentences. Be specific, reference actual answers from the transcript.

Also classify your post:
- post_type: one of [observation, concern, praise, question, strategy]
- sentiment: one of [positive, neutral, negative, mixed]

Return JSON:
```json
{{
  "content": "your forum post text",
  "post_type": "observation|concern|praise|question|strategy",
  "sentiment": "positive|neutral|negative|mixed"
}}
```"""

        system = f"""You are {observer.name}, {observer.role}. Personality: {observer.personality}.
You are posting in a private forum only visible to other interviewers.
Be honest, specific, and constructive. Reference actual candidate answers."""

        try:
            result = self.llm.generate_json(prompt=prompt, system_prompt=system, temperature=0.6)

            post_id = self.db.create_post(
                session_id=session_id,
                agent_id=observer.name.lower().replace(" ", "_"),
                agent_name=observer.name,
                content=result["content"],
                topic=f"round_{round_num}_observation",
                post_type=result.get("post_type", "observation"),
                agent_type=observer.role,
                round_num=round_num,
            )

            return ForumPost(
                agent_name=observer.name,
                agent_role=observer.role,
                content=result["content"],
                post_type=result.get("post_type", "observation"),
                sentiment=result.get("sentiment", "neutral"),
                round_num=round_num,
                post_id=post_id,
            )
        except Exception as e:
            logger.error(f"Failed to generate observation for {observer.name}: {e}")
            return None

    def _generate_replies(
        self,
        session_id: str,
        round_num: int,
        posts: List[ForumPost],
        panel: List[InterviewerPersona],
    ):
        """Generate 1-2 replies between observers to make the forum feel alive."""
        if len(posts) < 2:
            return

        # Pick one observer to reply to another's post
        replier_post = posts[0]
        target_post = posts[1]

        replier = next((p for p in panel if p.name == replier_post.agent_name), None)
        if not replier or not target_post.post_id:
            return

        prompt = f"""You are {replier.name} ({replier.role}) in the private interviewer forum.

{target_post.agent_name} ({target_post.agent_role}) just posted:
"{target_post.content}"

Write a short reply (1-2 sentences). You can agree, disagree, add context, or ask a follow-up question. Be natural and conversational.

Return JSON:
```json
{{"reply": "your reply text"}}
```"""

        try:
            result = self.llm.generate_json(prompt=prompt, temperature=0.7)
            reply_text = result.get("reply", "")
            if reply_text:
                self.db.create_comment(
                    post_id=target_post.post_id,
                    session_id=session_id,
                    agent_id=replier.name.lower().replace(" ", "_"),
                    agent_name=replier.name,
                    content=reply_text,
                    comment_type="reply",
                    round_num=round_num,
                )
                target_post.replies.append({
                    "agent_name": replier.name,
                    "content": reply_text,
                })
        except Exception as e:
            logger.error(f"Failed to generate reply: {e}")

    def run_live_observation(
        self,
        session_id: str,
        round_num: int,
        active_interviewer: str,
        question_num: int,
        last_question: str,
        last_answer: str,
        panel: List[InterviewerPersona],
        candidate_summary: str = "",
    ) -> List[ForumPost]:
        """
        During an active round: observers post short, focused live reactions
        every 2-3 questions. These are shorter than end-of-round posts.
        Fired asynchronously — doesn't block the interview flow.
        """
        observers = [p for p in panel if p.name != active_interviewer]
        if not observers:
            return []

        # Only 1-2 observers react per question to keep it natural
        import random
        reacting = random.sample(observers, min(len(observers), 2))

        posts: List[ForumPost] = []
        with ThreadPoolExecutor(max_workers=len(reacting)) as pool:
            futures = {
                pool.submit(
                    self._generate_live_reaction,
                    session_id, round_num, observer,
                    active_interviewer, question_num,
                    last_question, last_answer, candidate_summary,
                ): observer
                for observer in reacting
            }
            for future in as_completed(futures):
                try:
                    post = future.result()
                    if post:
                        posts.append(post)
                except Exception as e:
                    logger.error(f"Live observer failed: {e}")

        return posts

    def _generate_live_reaction(
        self,
        session_id: str,
        round_num: int,
        observer: InterviewerPersona,
        active_interviewer: str,
        question_num: int,
        last_question: str,
        last_answer: str,
        candidate_summary: str,
    ) -> Optional[ForumPost]:
        """Generate a short live reaction from an observer during an active round."""
        prompt = f"""You are {observer.name} ({observer.role}), observing a live interview by {active_interviewer} (Question #{question_num}).

## Your Focus Areas
{', '.join(observer.eval_dimensions)}

## Latest Exchange
Q: {last_question}
A: {last_answer}

{f'## Candidate Background{chr(10)}{candidate_summary}' if candidate_summary else ''}

---

Write a short live reaction (1-2 sentences). You can:
- Flag something the candidate said that's worth probing
- Suggest a follow-up direction for {active_interviewer}
- Note a strength or red flag from your expertise area
- Point out if the candidate is being evasive or contradictory

Be concise — this is a quick note in the live chat, not a formal review.

Return JSON:
```json
{{"content": "your reaction", "post_type": "observation|concern|praise|suggestion", "sentiment": "positive|neutral|negative"}}
```"""

        system = f"You are {observer.name}, {observer.role}. Write a brief live reaction. 1-2 sentences max."

        try:
            result = self.llm.generate_json(prompt=prompt, system_prompt=system, temperature=0.7)

            post_id = self.db.create_post(
                session_id=session_id,
                agent_id=observer.name.lower().replace(" ", "_"),
                agent_name=observer.name,
                content=result["content"],
                topic=f"round_{round_num}_live_q{question_num}",
                post_type=result.get("post_type", "observation"),
                agent_type=observer.role,
                round_num=round_num,
            )

            return ForumPost(
                agent_name=observer.name,
                agent_role=observer.role,
                content=result["content"],
                post_type=result.get("post_type", "observation"),
                sentiment=result.get("sentiment", "neutral"),
                round_num=round_num,
                post_id=post_id,
            )
        except Exception as e:
            logger.error(f"Live reaction failed for {observer.name}: {e}")
            return None

    def get_live_suggestions(self, session_id: str, round_num: int) -> str:
        """
        Build a digest of live observer reactions for the active interviewer.
        Used to inject mid-round suggestions into question generation.
        """
        posts = self.db.get_session_posts(session_id)
        live_posts = [
            p for p in posts
            if p.get("round_num") == round_num
            and "live_q" in p.get("topic", "")
        ]

        if not live_posts:
            return ""

        lines = ["## Live Observer Notes (private):"]
        for p in live_posts:
            lines.append(f"- {p['agent_name']}: {p['content']}")
        return "\n".join(lines)

    def get_forum_digest(
        self, session_id: str, for_agent: str, up_to_round: int
    ) -> str:
        """
        Build a digest of forum posts for a specific interviewer.
        Used to inject context into the next round's interviewer prompt.
        """
        return self.db.build_forum_digest(session_id, up_to_round)

    def get_full_forum(self, session_id: str) -> List[dict]:
        """
        Get the complete forum for the reveal page.
        Returns posts grouped by round with comments.
        """
        all_rounds = {}
        posts = self.db.get_session_posts(session_id)

        for p in posts:
            rn = p.get("round_num", 0)
            if rn not in all_rounds:
                all_rounds[rn] = []

            comments = self.db.get_comments_for_post(p["post_id"])
            p["comments"] = comments
            all_rounds[rn].append(p)

        result = []
        for round_num in sorted(all_rounds.keys()):
            result.append({
                "round_num": round_num,
                "posts": all_rounds[round_num],
            })
        return result

    def get_forum_summary(self, session_id: str) -> dict:
        """Get a summary of forum activity for the results page."""
        posts = self.db.get_session_posts(session_id)
        if not posts:
            return {"total_posts": 0, "total_comments": 0, "sentiment_breakdown": {}}

        total_comments = 0
        sentiments = {}
        by_agent = {}

        for p in posts:
            comments = self.db.get_comments_for_post(p["post_id"])
            total_comments += len(comments)

            agent = p["agent_name"]
            if agent not in by_agent:
                by_agent[agent] = {"posts": 0, "role": p.get("agent_type", "")}
            by_agent[agent]["posts"] += 1

        return {
            "total_posts": len(posts),
            "total_comments": total_comments,
            "by_agent": by_agent,
        }
