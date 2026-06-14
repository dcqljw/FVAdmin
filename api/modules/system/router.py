from fastapi import APIRouter, Depends, Security, UploadFile

from core.deps import verify_token_dep, get_current_user, permission_check
from shared.base_schema import SuccessResponse
from modules.system.models import User
from modules.system.schemas import (
    UserCreateSchema, EditPasswordSchema,
    RoleCreateSchema, MenuCreateSchema, MenuEditSchema, AddRoleMenuSchema,
)
from modules.system.service import user_service, role_service, menu_service

# ========== 子路由（各自带 prefix） ==========

user_router = APIRouter(prefix="/user", tags=["用户管理"])
role_router = APIRouter(prefix="/role", tags=["角色管理"])
menu_router = APIRouter(prefix="/menu", tags=["菜单管理"])


# ========== User ==========

@user_router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    user_dict = await user_service.get_user_info(user)
    return SuccessResponse(data=user_dict)


@user_router.get("")
async def get_user_list(
        user: User = Depends(get_current_user),
        current: int = 1,
        size: int = 10,
        username: str = None,
        phone: str = None,
        email: str = None,
):
    user_list, total = await user_service.list_users(
        current=current, size=size,
        username=username, phone=phone, email=email,
    )
    return SuccessResponse(data={"records": user_list, "total": total})


@user_router.post("/add")
async def add_user(
        user_in: UserCreateSchema,
        current_user: User = Security(permission_check, scopes=['user:add']),
):
    await user_service.create_user(
        username=user_in.username, password=user_in.password,
        nickname=user_in.nickname, role_codes=user_in.role,
        email=user_in.email, phone=user_in.phone, avatar=user_in.avatar,
    )
    return SuccessResponse(data={"msg": "添加用户成功"})


@user_router.post('/edit')
async def edit_user(
        user_in: UserCreateSchema,
        current_user: User = Security(permission_check, scopes=['user:edit']),
):
    await user_service.update_user(
        username=user_in.username, nickname=user_in.nickname,
        role_codes=user_in.role, email=user_in.email,
        phone=user_in.phone, avatar=user_in.avatar,
    )
    return SuccessResponse(data={"msg": "修改用户成功"})


@user_router.post('/edit-profile')
async def edit_profile(
        user_in: UserCreateSchema,
        current_user: User = Depends(get_current_user),
):
    await user_service.update_profile(
        user=current_user, nickname=user_in.nickname,
        email=user_in.email, phone=user_in.phone, avatar=user_in.avatar,
    )
    return SuccessResponse(data={"msg": "修改用户成功"})


@user_router.post('/upload_avatar')
async def upload_avatar(
        file: UploadFile,
        current_user: User = Depends(get_current_user),
):
    file_content = await file.read()
    avatar_url = await user_service.upload_avatar(
        user=current_user, file_content=file_content,
        filename=file.filename, content_type=file.content_type,
        file_size=file.size,
    )
    return SuccessResponse(data={"msg": "上传成功", "avatar_url": avatar_url})


@user_router.post('/delete')
async def delete_user(
        user_id: int,
        current_user: User = Security(permission_check, scopes=['user:delete']),
):
    await user_service.delete_user(user_id=user_id, current_user=current_user)
    return SuccessResponse(data={"msg": "删除用户成功"})


@user_router.post('/edit-password')
async def edit_password(
        password_in: EditPasswordSchema,
        current_user: User = Depends(get_current_user),
):
    await user_service.change_password(
        user=current_user,
        old_password=password_in.old_password,
        new_password=password_in.new_password,
    )
    return SuccessResponse(data={"msg": "修改密码成功"})


@user_router.post('/reset-password')
async def reset_password(
        user_id: int,
        current_user: User = Security(permission_check, scopes=['user:reset-password']),
):
    username, new_password = await user_service.reset_password(user_id=user_id)
    return SuccessResponse(data={"new_password": new_password})


# ========== Role ==========

@role_router.get("")
async def get_role_list(
        current: int = 1,
        size: int = 10,
        name: str = None,
        code: str = None,
        description: str = None,
):
    role_list, total = await role_service.list_roles(
        current=current, size=size, name=name, code=code, description=description,
    )
    return SuccessResponse(data={"records": role_list, "total": total})


@role_router.post("/add")
async def add_role(
        role: RoleCreateSchema,
        current_user: User = Security(permission_check, scopes=['role:add']),
):
    await role_service.create_role(
        name=role.name, code=role.code,
        description=role.description, enabled=role.enabled,
    )
    return SuccessResponse(data={"msg": "添加角色成功"})


@role_router.post('/delete')
async def delete_role(
        role_id: int,
        current_user: User = Security(permission_check, scopes=['role:delete']),
):
    await role_service.delete_role(role_id=role_id, current_user=current_user)
    return SuccessResponse(data={"msg": "删除角色成功"})


@role_router.post('/edit')
async def edit_role(
        role_in: RoleCreateSchema,
        current_user: User = Security(permission_check, scopes=['role:edit']),
):
    await role_service.update_role(
        code=role_in.code, name=role_in.name,
        description=role_in.description, enabled=role_in.enabled,
    )
    return SuccessResponse(data={"msg": "修改角色成功"})


@role_router.get("/{role_id}/user")
async def role_user(
        role_id: int,
        user: User = Depends(get_current_user),
        current: int = 1,
        size: int = 10,
        username: str = None,
        phone: str = None,
        email: str = None,
):
    """
    根据角色ID返回该角色下的所有用户
    """
    user_list, total = await user_service.list_users(
        role_id=role_id,
        current=current, size=size,
        username=username, phone=phone, email=email,
    )
    return SuccessResponse(data={"records": user_list, "total": total})


# ========== Menu ==========

@menu_router.get("")
async def menu_list(
        current_user: User = Security(permission_check, scopes=['menu:list']),
):
    """
    获取全量菜单树（菜单管理页使用）
    需要 menu:list 权限
    """
    tree = await menu_service.get_all_menu_tree()
    return SuccessResponse(data=tree)


@menu_router.get("/route")
async def route_menu_list(current_user: User = Depends(get_current_user)):
    """
    获取当前用户有权限的菜单树（侧边栏导航/路由注册使用）
    只需登录即可，返回按角色过滤后的菜单，自动补全祖先链
    """
    tree = await menu_service.get_user_menu_tree(current_user)
    return SuccessResponse(data=tree)


@menu_router.get("/get_checked")
async def get_checked(role_id: int, uid: str = Depends(verify_token_dep)):
    """
    根据角色id获取对应的权限
    """
    leaf_menu_ids = await menu_service.get_role_menu_ids(role_id)
    return SuccessResponse(data=leaf_menu_ids)


@menu_router.post("/add")
async def add_menu(
        menu: MenuCreateSchema,
        current_user: User = Security(permission_check, scopes=['menu:add']),
):
    await menu_service.create_menu(
        parent_id=menu.parent_id, name=menu.name, path=menu.path,
        meta=menu.meta, component=menu.component, sort=menu.sort,
        status=menu.status, auth_mark=menu.auth_mark, menu_type=menu.type,
    )
    return SuccessResponse(data={"message": "添加菜单成功"})


@menu_router.post("/edit")
async def edit_menu(
        menu_in: MenuEditSchema,
        current_user: User = Security(permission_check, scopes=['menu:edit']),
):
    await menu_service.update_menu(
        menu_id=menu_in.id, name=menu_in.name, path=menu_in.path, meta=menu_in.meta,
        component=menu_in.component, sort=menu_in.sort,
        status=menu_in.status, auth_mark=menu_in.auth_mark, menu_type=menu_in.type,
    )
    return SuccessResponse(data={"message": "修改菜单成功"})


@menu_router.post("/add_menu_permission")
async def add_menu_permission(role_menu: AddRoleMenuSchema):
    """
    角色添加菜单权限
    """
    await menu_service.assign_menus_to_role(
        role_id=role_menu.role_id, menu_ids=role_menu.menu_ids,
    )
    return SuccessResponse(data={"message": "添加菜单成功"})


@menu_router.post("/delete")
async def delete_menu(
        menu_id: int,
        current_user: User = Security(permission_check, scopes=['menu:delete']),
):
    await menu_service.delete_menu(menu_id=menu_id)
    return SuccessResponse(data={"message": "删除菜单成功"})


# ========== 父路由：聚合所有子路由（供 auto-discover 发现） ==========

router = APIRouter(prefix="/system")
router.include_router(user_router)
router.include_router(role_router)
router.include_router(menu_router)
