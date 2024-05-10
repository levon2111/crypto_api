import platform

import psutil
from fastapi import APIRouter

router = APIRouter()


@router.get('/', include_in_schema=False)
@router.get('')
async def health():
    system_info = {
        "system": platform.system(),
        "processor": platform.processor(),
        "architecture": platform.architecture(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage('/')._asdict()
    }

    return {
        "system_info": system_info
    }
