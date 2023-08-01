from fastapi import APIRouter

from papihub.common.response import json_200

router = APIRouter()


@router.get("/api/torrents/list")
def is_processing():
    return json_200(data=[])
