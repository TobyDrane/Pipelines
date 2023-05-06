from typing import Optional
from pydantic import BaseModel, validator

class Pipeline(BaseModel):
    function_name: str
    next_function: Optional[str] = None

class Config(BaseModel):
    pipelines: list[Pipeline]

    @validator("pipelines")
    def check_for_only_one_termination(cls, value: list[Pipeline]):
        nones_found = 0
        for pipeline in value:
            if pipeline.next_function is None:
                nones_found += 1
            if nones_found > 1:
                raise ValueError("Pipeline config can only contain one termination step")
        return value