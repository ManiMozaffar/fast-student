import json

from pydantic import BaseModel


def pydantic_to_dict(model: BaseModel) -> dict:
    return json.loads(model.model_dump_json())
