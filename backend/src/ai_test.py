import asyncio
from os import getenv

from loguru import logger

from src.ai.categories_processor import separate_categories
from src.ai.graph_data_describer import describe_graph_data
from src.ai.manager import Manager
from src.ai.saving_category_content_generator import generate_saving_category_content
from src.ai.data_structures import CategoryInformation, StatisticalInformation, UserInformation
from src.ai.user_notes_content_generator import generate_notes_content


async def test():
    model = "gpt-4o-mini"
    api_key = getenv("api_key")
    manager = Manager(model, api_key)

    # logger.info(
    #     await generate_saving_category_content(
    #         manager,
    #         CategoryInformation("Taxi", 50, "EUR", 5),
    #         StatisticalInformation("Bolt"),
    #         "I would like to save some money on the secondary expenses. Still, I want to visit cafe 2 times a month and I maybe I’ll need taxi in some unexpected cases."
    #     )
    # )

    # logger.info(
    #     await generate_notes_content(
    #         manager,
    #         UserInformation(
    #             "I would like to save some money on the secondary expenses. Still, I want to visit cafe 2 times a month and I maybe I’ll need taxi in some unexpected cases.",
    #             "Danylo",
    #             19,
    #             "male"
    #         )
    #     )
    # )

    # logger.info(
    #     await separate_categories(
    #         manager,
    #         ["Restaurants", "Food", "Car", "Taxi", "Health"],
    #         """
    #         I would like to save some money on the secondary expenses.
    #         Still, I want to visit cafe 2 times a month and I maybe I’ll need taxi in some unexpected cases.
    #         """
    #     )
    # )

    logger.info(
        await describe_graph_data(
            manager,
            """{"categories": [{"category": "auto", "item_count": 44, "total_price": 105.04138}, {"category": "baby", "item_count": 155, "total_price": 317.79}, {"category": "basic", "item_count": 864, "total_price": 2720.82196}, {"category": "dairy", "item_count": 864, "total_price": 1882.776173}, {"category": "drinks", "item_count": 462, "total_price": 1397.11463}, {"category": "drugstore", "item_count": 170, "total_price": 838.8}, {"category": "eating", "item_count": 31, "total_price": 152.47}, {"category": "fashion", "item_count": 36, "total_price": 735.48}, {"category": "free-time", "item_count": 160, "total_price": 1728.93544}, {"category": "frozen", "item_count": 78, "total_price": 324.6792}, {"category": "fruits-veg", "item_count": 1095, "total_price": 2417.349992}, {"category": "hazard", "item_count": 1, "total_price": 5.5}, {"category": "health", "item_count": 167, "total_price": 861.23}, {"category": "home", "item_count": 959, "total_price": 3914.50409}, {"category": "meat", "item_count": 493, "total_price": 2991.59122}, {"category": "pastry", "item_count": 569, "total_price": 1102.25809}, {"category": "pets", "item_count": 9, "total_price": 74.95}, {"category": "seasonal", "item_count": 5, "total_price": 8.11}, {"category": "snacks", "item_count": 493, "total_price": 1255.548081}]}""",
            UserInformation(
                "I would like to save some money on the secondary expenses. Still, I want to visit cafe 2 times a month and I maybe I’ll need taxi in some unexpected cases.",
                "Danylo",
                19,
                "male"
            )
        )
    )


if __name__ == "__main__":
    asyncio.run(test())
