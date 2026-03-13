from fastapi import APIRouter, HTTPException
from typing import List
from models.sys_roles import RoleCreate, RoleOut
import crud.sys_roles_crud as sys_roles_crud

router = APIRouter(prefix="/sys_roles", tags=["Roles"])

@router.get("/", response_model=List[RoleOut])
def read_roles():
    result = sys_roles_crud.get_all_roles()
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", response_model=RoleOut)
def create_role(role: RoleCreate):
    result = sys_roles_crud.add_role(role)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/{role_id}", response_model=RoleOut)
def read_role(role_id: str):
    result = sys_roles_crud.get_role_by_id(role_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@router.put("/{role_id}", response_model=dict)
def update_role(role_id: str, role: RoleCreate):
    result = sys_roles_crud.update_role(role_id, role)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.delete("/{role_id}", response_model=dict)
def delete_role(role_id: str):
    result = sys_roles_crud.delete_role(role_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result