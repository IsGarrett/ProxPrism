from pydantic import BaseModel, Field

class LXCResponse(BaseModel):
    vmid: int
    name: str
    status: str
    cpu: float
    memory: int = Field(alias="mem")

    model_config = {"populate_by_name": True}