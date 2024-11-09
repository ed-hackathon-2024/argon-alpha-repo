from loguru import logger

from .data_structures import UserInformation
from .exceptions import ResponseNotGeneratedError
from .manager import Manager


async def describe_graph_data(manager: Manager, graph_data: dict, user_information: UserInformation) -> str:
    logger.info("Describing graph data for user goals: {}", user_information.goal)

    system_prompt = f"""
    You will receive the financial goals of the user and the graph information.
    Also, you'll receive user's personal data.

    Your task is to provide some small personalised conclusions (250-chars max) for the user to save more money 
    considering his financial goals. Act as a coach and tell the user some important conclusions from the 
    received data. 
    """

    user_content = f"""
    Goals: "{user_information.goal}"
    Graph information: "{graph_data}"
    Personal data:  "name: {user_information.name}, age: {user_information.age}, gender: {user_information.gender}"
    """

    response = await manager.client.chat.completions.create(
        model=manager.model,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_content
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )

    response_content = response.choices[0].message.content
    if response_content is None:
        raise ResponseNotGeneratedError()

    return response_content
