from fastapi import APIRouter

from papihub.common.response import json_200
from pydantic import BaseModel

router = APIRouter()


class AddParam(BaseModel):
    site_id: str
    auth_type: str
    auth_config: dict


@router.post("/api/site/add")
def add(param: AddParam):
    return json_200(data=[])
