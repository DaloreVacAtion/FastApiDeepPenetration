from typing import Optional

from pydantic import BaseModel


class ServiceResult(BaseModel):
    ok: bool
    message: str | None = None
