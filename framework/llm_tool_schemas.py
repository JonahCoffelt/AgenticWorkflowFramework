from pydantic import BaseModel, Field
from typing import Literal

class MessageRequest(BaseModel):
    content: str
    recivers: list[int]

class SetTaskOutputRequest(BaseModel):
    data: str

class SetTaskStatusRequest(BaseModel):
    status: int

message_request_schema = MessageRequest.model_json_schema()
set_task_output_request_schema = SetTaskOutputRequest.model_json_schema()
set_task_status_request_schema = SetTaskStatusRequest.model_json_schema()