"""Conversation history manager for maintaining context across messages."""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConversationMessage:
    """Represents a single message in conversation history."""
    author: str
    content: str
    timestamp: datetime
    
    def __str__(self) -> str:
        """Format message for display."""
        return f"{self.author}: {self.content}"


class ConversationHistory:
    """Manages conversation history per channel/thread."""
    
    def __init__(self, max_history_size: int = 5):
        """
        Initialize conversation history manager.
        
        :param max_history_size: Maximum number of messages to keep per conversation
        """
        self.max_history_size = max_history_size
        # Store history per channel/thread ID
        # Key: channel_id, Value: List[ConversationMessage]
        self._history: Dict[int, List[ConversationMessage]] = {}
        logger.info(f"ConversationHistory initialized with max_history_size={max_history_size}")
    
    def add_message(self, channel_id: int, author: str, content: str) -> None:
        """
        Add a message to the conversation history for a channel.
        
        :param channel_id: Discord channel/thread ID
        :param author: Message author (username or mention)
        :param content: Message content
        """
        if channel_id not in self._history:
            self._history[channel_id] = []
        
        message = ConversationMessage(
            author=author,
            content=content,
            timestamp=datetime.now()
        )
        
        self._history[channel_id].append(message)
        
        # Keep only the last max_history_size messages
        if len(self._history[channel_id]) > self.max_history_size:
            removed = self._history[channel_id].pop(0)
            logger.debug(f"Removed oldest message from channel {channel_id}: {removed.author}")
        
        logger.debug(f"Added message to channel {channel_id} history (total: {len(self._history[channel_id])})")
    
    def get_history(self, channel_id: int) -> List[ConversationMessage]:
        """
        Get conversation history for a channel.
        
        :param channel_id: Discord channel/thread ID
        :return: List of conversation messages (up to max_history_size)
        """
        return self._history.get(channel_id, [])
    
    def format_history_for_llm(self, channel_id: int, bot_name: str = "Friendbot") -> str:
        """
        Format conversation history as a string for the LLM.
        
        Sanitizes "Fuckbot" to "Friendbot" to avoid triggering safety filters.
        
        :param channel_id: Discord channel/thread ID
        :param bot_name: Name of the bot (for context)
        :return: Formatted conversation history string
        """
        history = self.get_history(channel_id)
        
        if not history:
            return ""
        
        # Build formatted history
        lines = [
            "Here is the recent conversation history in this channel:",
            ""
        ]
        
        for msg in history:
            # Skip bot's own messages in history (we're generating a response)
            if bot_name.lower() in msg.author.lower() or "bot" in msg.author.lower():
                continue
            
            # Sanitize "Fuckbot" to "Friendbot" before sending to LLM
            sanitized_content = msg.content.replace("Fuckbot", "Friendbot")
            sanitized_author = msg.author.replace("Fuckbot", "Friendbot")
            lines.append(f"{sanitized_author}: {sanitized_content}")
        
        formatted = "\n".join(lines)
        logger.debug(f"Formatted history for channel {channel_id} ({len(history)} messages, {len(formatted)} chars)")
        return formatted
    
    def clear_history(self, channel_id: int) -> None:
        """
        Clear conversation history for a channel.
        
        :param channel_id: Discord channel/thread ID
        """
        if channel_id in self._history:
            del self._history[channel_id]
            logger.info(f"Cleared history for channel {channel_id}")
    
    def clear_all_history(self) -> None:
        """Clear all conversation history."""
        count = len(self._history)
        self._history.clear()
        logger.info(f"Cleared all conversation history ({count} channels)")

