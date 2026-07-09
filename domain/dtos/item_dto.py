from pydantic import BaseModel

from data.model.item_type import ItemType

ItemTypeDto = ItemType


class ItemDto(BaseModel):
    type: ItemTypeDto
    durability: int
