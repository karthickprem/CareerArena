"""
Arena — full Reddit-style forum for career agent debate.
Mirrors Debug Arena's Forum class with action logging, personalized feeds,
likes/dislikes/follows, and search.
"""

from __future__ import annotations

from typing import Optional

from database import CareerDB


class PostResult:
    def __init__(self, post_id: int, agent_id: str, agent_name: str, content: str):
        self.post_id = post_id
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.content = content


class CommentResult:
    def __init__(self, comment_id: int, post_id: int, parent_comment_id: Optional[int] = None):
        self.comment_id = comment_id
        self.post_id = post_id
        self.parent_comment_id = parent_comment_id


class Arena:
    """Reddit-style arena where career agents debate. Wraps CareerDB with action logging."""

    def __init__(self, db: Optional[CareerDB] = None):
        self.db = db or CareerDB()

    def create_post(
        self,
        session_id: str,
        agent_id: str,
        agent_name: str,
        agent_type: str,
        topic: str,
        content: str,
        post_type: str = "analysis",
        confidence: float = 0.5,
        evidence: str = "",
        round_num: int = 0,
    ) -> PostResult:
        post_id = self.db.create_post(
            session_id=session_id,
            agent_id=agent_id,
            agent_name=agent_name,
            content=content,
            topic=topic,
            post_type=post_type,
            agent_type=agent_type,
            confidence=confidence,
            evidence=[evidence] if evidence else [],
            round_num=round_num,
        )
        self.db.log_action(session_id, round_num, agent_id, agent_name, "CREATE_POST", post_id, content[:500])
        return PostResult(post_id=post_id, agent_id=agent_id, agent_name=agent_name, content=content)

    def create_comment(
        self,
        session_id: str,
        post_id: int,
        agent_id: str,
        agent_name: str,
        content: str,
        comment_type: str = "response",
        round_num: int = 0,
        parent_comment_id: Optional[int] = None,
    ) -> Optional[CommentResult]:
        if not self.db.get_post(post_id):
            return None
        comment_id = self.db.create_comment(
            post_id=post_id,
            session_id=session_id,
            agent_id=agent_id,
            agent_name=agent_name,
            content=content,
            comment_type=comment_type,
            round_num=round_num,
            parent_comment_id=parent_comment_id,
        )
        action_type = "REPLY_COMMENT" if parent_comment_id else "CREATE_COMMENT"
        self.db.log_action(session_id, round_num, agent_id, agent_name, action_type,
                           parent_comment_id or post_id, content[:500])
        return CommentResult(comment_id=comment_id, post_id=post_id, parent_comment_id=parent_comment_id)

    def like_post(self, post_id: int, session_id: str, agent_id: str, agent_name: str, round_num: int = 0) -> None:
        self.db.like_post(post_id)
        self.db.log_action(session_id, round_num, agent_id, agent_name, "LIKE_POST", post_id)

    def dislike_post(self, post_id: int, session_id: str, agent_id: str, agent_name: str, round_num: int = 0) -> None:
        self.db.dislike_post(post_id)
        self.db.log_action(session_id, round_num, agent_id, agent_name, "DISLIKE_POST", post_id)

    def like_comment(self, comment_id: int, session_id: str, agent_id: str, agent_name: str, round_num: int = 0) -> None:
        self.db.like_comment(comment_id)
        self.db.log_action(session_id, round_num, agent_id, agent_name, "LIKE_COMMENT", comment_id)

    def dislike_comment(self, comment_id: int, session_id: str, agent_id: str, agent_name: str, round_num: int = 0) -> None:
        self.db.dislike_comment(comment_id)
        self.db.log_action(session_id, round_num, agent_id, agent_name, "DISLIKE_COMMENT", comment_id)

    def follow_agent(self, follower_id: str, followee_id: str, session_id: str,
                     follower_name: str, round_num: int = 0) -> None:
        self.db.follow(follower_id, followee_id, session_id)
        self.db.log_action(session_id, round_num, follower_id, follower_name, "FOLLOW", target_id=None,
                           content=f"followed {followee_id}")

    def search_posts(self, session_id: str, query: str) -> str:
        return self.db.search_posts(session_id, query)

    def get_feed(self, session_id: str, agent_id: str,
                 agent_keywords: list = None, max_posts: int = 15) -> str:
        return self.db.get_personalized_feed(session_id, agent_id, agent_keywords, max_posts)

    def get_session_posts(self, session_id: str) -> list:
        return self.db.get_session_posts(session_id)

    def get_post_comments(self, post_id: int) -> list:
        return self.db.get_comments_for_post(post_id)

    def get_stats(self, session_id: str) -> dict:
        return self.db.get_session_stats(session_id)

    def build_feed(self, session_id: str, for_agent: str = "") -> str:
        """Build a text feed of all arena activity for agent consumption."""
        posts = self.get_session_posts(session_id)
        if not posts:
            return "The arena is empty. No posts yet."

        lines = [f"## Arena Feed ({len(posts)} posts)\n"]

        for post in posts:
            pid = post["post_id"]
            badge = f"[{post.get('agent_type', 'agent')}]"
            conf = f" (confidence: {post.get('confidence', '?')})" if post.get('confidence') else ""
            topic_tag = f" #{post.get('topic', 'general')}" if post.get('topic') else ""

            lines.append(
                f"### Post #{pid} by {post['agent_name']} {badge}{topic_tag}{conf}"
            )
            lines.append(post["content"])

            comments = self.get_post_comments(pid)
            if comments:
                lines.append(f"\n  ({len(comments)} comments)")
                for c in comments:
                    ctype = f" [{c.get('comment_type', '')}]" if c.get('comment_type') else ""
                    prefix = "    └─" if c.get("parent_comment_id") else "  >"
                    lines.append(
                        f"{prefix} Comment #{c['comment_id']} by {c['agent_name']}{ctype}: "
                        f"{c['content'][:300]}"
                    )

            lines.append("")

        return "\n".join(lines)

    def build_transcript(self, session_id: str) -> str:
        return self.db.build_transcript(session_id)
