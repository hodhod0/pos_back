from fastapi import APIRouter, HTTPException
from typing import List
from models.role import RoleCreate, RoleOut
import crud.role_crud as role_crud

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RoleOut])
def read_roles():
    result = role_crud.get_all_roles()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", response_model=RoleOut)
def create_role(role: RoleCreate):
    result = role_crud.add_role(role)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/{role_id}", response_model=RoleOut)
def read_role(role_id: str):
    result = role_crud.get_role_by_id(role_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.put("/{role_id}", response_model=dict)
def update_role(role_id: str, role: RoleCreate):
    result = role_crud.update_role(role_id, role)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.delete("/{role_id}", response_model=dict)
def delete_role(role_id: str):
    result = role_crud.delete_role(role_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result