from pydantic import BaseModel
from typing import List, Optional


class Request(BaseModel):
    class Config:
        str_strip_whitespace = True


class Pagination(BaseModel):
    totalItems: int
    itemsPerPage: int
    currentPage: int
    totalPages: int
    nextPage: Optional[str] = None
    previousPage: Optional[str] = None


class DropdownItem(BaseModel):
    id: str
    value: str


class ListResponse(BaseModel):
    count: int
    data: List[BaseModel]
    pagination: Pagination


class DetailResponse(BaseModel):
    data: dict


class CreateResponse(BaseModel):
    message: str


class UpdateResponse(BaseModel):
    message: str
    updated_id: Optional[str] = None


class DeleteResponse(BaseModel):
    message: str
    deleted_id: Optional[str] = None


class DropdownResponse(BaseModel):
    data: List[DropdownItem]