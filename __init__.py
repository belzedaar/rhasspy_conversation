from __future__ import annotations

from functools import partial
import logging

from homeassistant.helpers import intent
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.conversation import agent
from homeassistant.components import conversation

from abc import abstractmethod

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize your integration."""
    conversation.async_set_agent(hass, RhasspyConversationAgent())

    return True

class RhasspyConversationAgent(agent.AbstractConversationAgent):

    @property
    def attribution(self) -> agent.Attribution:
        """Return the attribution."""
        return {
            "name": "Rhasspy Conversation Agent",
            "url": "https://github.com/belzedaar/rhasspy_conversation",
        }

    @abstractmethod
    async def async_process(self, user_input: agent.ConversationInput) -> agent.ConversationResult:
        """Process a sentence."""
        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech("Test response")
        return agent.ConversationResult(
            conversation_id=None,
            response=response
        )