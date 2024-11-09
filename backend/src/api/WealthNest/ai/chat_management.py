import asyncio
import json
from os import getenv
from loguru import logger

from .manager import Manager


class ChatAssistant:
    """Handles LLM chat interactions for financial goal coaching."""

    def __init__(self, initial_goal: str, manager: Manager):
        self.manager = manager
        self.thread = None
        self.assistant = None
        self.goal = initial_goal
        logger.debug(f"ChatAssistant initialized with goal: {initial_goal}")

    async def process_user_request(self, user_input: str) -> dict:
        """Analyze user input and generate LLM response."""

        if self.thread is None:
            system_instructions = f"""
            You are a finance and savings coach. 
            Respond to user inquiries about their financial goals, and suggest changes to their goals only 
            if they explicitly mention wanting to revise or change their plans. 
            If needed, call the suggest function only once and with a complete goal.

            The initial user goal is: {self.goal}
            """

            self.thread = await self.manager.client.beta.threads.create()
            self.assistant = await self.manager.client.beta.assistants.create(
                name="Financial coach",
                instructions=system_instructions,
                model=self.manager.model,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "suggest_user_goal",
                            "description": "Function to suggest a new user goal in the financial assistant",
                            "parameters": {
                                "type": "object",
                                "required": [
                                    "goal"
                                ],
                                "properties": {
                                    "goal": {
                                        "type": "string",
                                        "description": "The complete version of the suggested new user goal"
                                    }
                                },
                                "additionalProperties": False
                            },
                            "strict": True
                        }
                    }
                ],
                response_format={
                    "type": "text"
                }
            )
        await self.manager.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=user_input
        )

        run = await self.manager.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Respond to the user."
        )

        if run.status == 'completed':
            messages = await self.manager.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            logger.debug(messages)
        else:
            logger.debug(run.status)

        # Define the list to store tool outputs
        tool_outputs = []

        suggested_goal = None

        # Loop through each tool in the required action section
        if run.required_action is not None:
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                if tool.function.name == "suggest_user_goal":
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": "Success"
                    })
                suggested_goal = tool.function.arguments

        if tool_outputs:
            try:
                run = await self.manager.client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                logger.debug("Tool outputs submitted successfully.")
            except Exception as e:
                logger.debug("Failed to submit tool outputs:", e)
        else:
            logger.debug("No tool outputs to submit.")

        messages = None

        if run.status == 'completed':
            messages = await self.manager.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            logger.debug(messages)
        else:
            logger.debug(run.status)

        return {
            "response": messages.data[0].content[0].text.value,
            "suggested_goal": json.loads(suggested_goal)["goal"] if suggested_goal else None
        }

    async def handle_goal_feedback(self, is_approved: bool):
        """Handle user feedback for suggested goal change."""
        raise NotImplementedError


async def example():
    model = "gpt-4o-mini"
    api_key = getenv("api_key")
    manager = Manager(model, api_key)
    assistant = ChatAssistant(initial_goal="Save money for a vacation", manager=manager)

    # Step 1: User asks for general advice
    user_input = "What should I do to start saving better?"
    response = await assistant.process_user_request(user_input)
    print("Assistant:", response)

    # Step 2: User indicates they want to revise their goal
    user_input = "I think I want to change my goal to saving for a new car."
    response = await assistant.process_user_request(user_input)
    print("Assistant:", response)


if __name__ == "__main__":
    asyncio.run(example())