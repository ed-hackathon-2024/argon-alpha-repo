import json

from loguru import logger

from .exceptions import ResponseNotGeneratedError
from .manager import Manager


async def separate_categories(manager: Manager, categories, user_goals: str) -> dict:
    logger.info("Separating categories for user goals: {}", user_goals)

    system_prompt = f"""
    You will receive the list of categories and the user's goals.
    Your task is to separate those categories into two groups:
    - The primary categories, which the user should focus on to save money.
    - The secondary categories, on which the user can save less money due to their importance.
    
    From your response, remove the most life-important categories, on which the user can't save money at all.
    """

    response = await manager.client.chat.completions.create(
        model="gpt-4o-mini",
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
                        "text": f"Goals: {user_goals}\n"
                                f"Categories: {categories}"
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
            "type": "json_schema",
            "json_schema": {
                "name": "category_separation",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "primary_categories": {
                            "type": "array",
                            "description": "Categories that the user should focus on to save money.",
                            "items": {
                                "type": "string",
                                "description": "The name of a primary category."
                            }
                        },
                        "secondary_categories": {
                            "type": "array",
                            "description": "Categories on which the user can save less money due to their importance.",
                            "items": {
                                "type": "string",
                                "description": "The name of a secondary category."
                            }
                        }
                    },
                    "required": [
                        "primary_categories",
                        "secondary_categories"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    response_content = response.choices[0].message.content
    if response_content is None:
        raise ResponseNotGeneratedError()

    return json.loads(response_content)
