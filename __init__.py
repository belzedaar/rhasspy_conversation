from __future__ import annotations

from functools import partial
import logging

from homeassistant.helpers import intent
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.conversation import agent
from homeassistant.components import conversation

from aiohttp import BasicAuth, FormData
from aiohttp.client_exceptions import ClientError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Initialize your integration."""

    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    conversation.async_set_agent(hass, entry, RhasspyConversationAgent(hass, entry))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Rhasspy Conversation."""
    conversation.async_unset_agent(hass, entry)
    return True

class RhasspyConversationAgent(agent.AbstractConversationAgent):

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the agent."""
        self.hass = hass
        self.entry = entry
        self.host = entry.data["host"]
        _LOGGER.info(f"Host: {self.host}")

    @property
    def attribution(self) -> agent.Attribution:
        """Return the attribution."""
        return {
            "name": "Rhasspy Conversation Agent",
            "url": "https://github.com/belzedaar/rhasspy_conversation",
        }

    async def async_process(self, user_input: agent.ConversationInput) -> agent.ConversationResult:
        """Process a sentence."""
        session = aiohttp_client.async_get_clientsession(self.hass)
        url = self.host + "/api/text-to-intent?nohass=false&outputFormat=rhasspy"
        text_response = "Sorry, Dave"
        headers = {'accept': 'application/json'}
        try:
            async with session.post(url, json=user_input.text, headers=headers) as response:
                json = await response.json()
                _LOGGER.debug("JSON: %r", json)
                if json["intent"]["name"] == "":
                    text_response = "I don't understand your banter"
                else:
                    text_response = "Job Done"

        except ClientError as err:
            _LOGGER.error("Error while intent message: %r", err)

        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech(text_response)
        return agent.ConversationResult(
            conversation_id=None,
            response=response
        )