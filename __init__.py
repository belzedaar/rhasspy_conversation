from homeassistant.helpers import intent

from homeassistant.components.conversation import agent
from homeassistant.components import conversation

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Initialize your integration."""
    conversation.async_set_agent(hass, entry, RhasspyConversationAgent())


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