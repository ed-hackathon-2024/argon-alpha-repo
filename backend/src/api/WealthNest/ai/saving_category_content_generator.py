import json

from loguru import logger

from .data_structures import CategoryInformation, StatisticalInformation
from .exceptions import ResponseNotGeneratedError
from .manager import Manager


async def generate_saving_category_content(
        manager: Manager,
        category: CategoryInformation,
        statistical_information: StatisticalInformation | None,
        user_goal: str
) -> dict:
    logger.info("Generating saving category {} tile content.", category)

    statistical_information = f"""
    In this category, the user often makes transactions for “{statistical_information.common_transaction_name}”.
    """ if statistical_information.common_transaction_name else ""

    average = category.monthly_expenses / category.transactions_amount

    system_prompt = f"""
    Imagine you are a budget management coach. Your task is to help the user save money effectively.

    The user’s monthly expenses in the "{category.name}" category are {category.monthly_expenses} {category.currency}, with {category.transactions_amount} transaction(s) per month. The average expense per transaction in this category is {average:.2f} {category.currency}.

    {statistical_information}

    The user wants to reduce spending in this category significantly, specifically aiming to lower expenses to support only their essential needs. They indicated that their target is to limit their usage in this category to approximately 2 transactions per month, rather than the current number of transactions.

    Define a **realistic target monthly expense (goal)** for this category that meets the user’s minimal requirements and reflects only the essential expenses.

    Provide recommendations based on the average transaction cost, aligning with the user’s target number of transactions and the possibility of cutting back on non-essential spending.
    """

    logger.debug("Sending prompt to OpenAI: {}", system_prompt)

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
                        "text": user_goal
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
                "name": "budget_management",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "goal": {
                            "type": "integer",
                            "description": "The goal amount for the user to spend on this category."
                        },
                        "overview": {
                            "type": "string",
                            "description": "A brief overview of how much money the user could save, limited to two sentences."
                        },
                        "transaction_based_response": {
                            "type": "string",
                            "description": "Advice on how the user can reach their goal based on transactions and mentioning them, limited to two sentences."
                        }
                    },
                    "required": [
                        "goal",
                        "overview",
                        "transaction_based_response"
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
