# from typing import NamedTuple

# from loguru import logger
# import json

# from .exceptions import ResponseNotGeneratedError
# from .manager import  Manager

# from ...WealthNest.getCategories import get_unique_categories


# # class UserInformation(NamedTuple):
# #     goal: str
# #     name: str
# #     age: int
# #     gender: str


# async def determine_secondary_categories(manager: Manager) -> dict:
#     logger.info("Generating notes content for user goal: {}", user_information.goal)

#     system_prompt = f"""
#     The user will message you with his goals. 
#     Give the user a personalised motivational story to save more money. 
#     Max. response size: 3 sentences. 
#     In the story, mention financial behavior patterns/financial personalities suitable for the user. 
#     Tell the user, which category is he matching right now, which category may be his target.\n\n
#     Maybe helpful patterns:\n
#     - Spender\n
#     - Saver\n
#     - Investor\n
#     - Debt Avoider\n
#     - Big Spender\n
#     - Hoarder\n
#     - Risk Taker\n
#     - Financially Indifferent\n\n
#     User's personal information:\n
#     name: {user_information.name}\n
#     age: {user_information.age}\n
#     gender: {user_information.gender}
#     """

#     response = await manager.client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {
#                 "role": "system",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": system_prompt
#                     }
#                 ]
#             },
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": user_information.goal
#                     }
#                 ]
#             }
#         ],
#         temperature=1,
#         max_tokens=2048,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#         response_format={
#             "type": "json_schema",
#             "json_schema": {
#                 "name": "motivational_story",
#                 "strict": True,
#                 "schema": {
#                     "type": "object",
#                     "properties": {
#                         "goals": {
#                             "type": "array",
#                             "description": "List of goals or aspirations the user has regarding saving money.",
#                             "items": {
#                                 "type": "string"
#                             }
#                         },
#                         "story": {
#                             "type": "string",
#                             "description": "A motivational story related to saving money."
#                         }
#                     },
#                     "required": [
#                         "goals",
#                         "story"
#                     ],
#                     "additionalProperties": False
#                 }
#             }
#         }
#     )

#     response_content = response.choices[0].message.content
#     if response_content is None:
#         raise ResponseNotGeneratedError()

#     return json.loads(response_content)
