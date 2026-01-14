def convert_menu_to_tree(menu_list: list[dict]) -> list[dict]:
    """
    将扁平的菜单列表转换为嵌套的树形结构
    规则：
    - type=1: 菜单节点，子菜单挂载到 children；按钮作为 authList 挂载到 meta 下
    - type=2: 按钮节点，仅作为菜单节点的 meta.authList 存在，无下级子节点
    :param menu_list: 数据库查询的扁平菜单列表（字典列表）
    :return: 嵌套的菜单树形结构（仅返回顶级菜单，按钮包含在菜单的 meta.authList 中）
    """
    # 1. 预处理：过滤无效数据 + 构建父ID映射（区分菜单/按钮）
    parent_map = {}
    for menu in menu_list:
        # 基础字段校验（避免空值）
        menu_id = menu.get("id")
        parent_id = menu.get("parent_id", 0)
        menu_type = menu.get("type", 1)  # 默认1=菜单

        # 跳过无效数据
        if not menu_id:
            continue

        # 初始化父ID映射（key: parent_id, value: {"menus": [], "buttons": []}）
        if parent_id not in parent_map:
            parent_map[parent_id] = {"menus": [], "buttons": []}

        # 按类型分类存储（菜单/按钮/目录）
        if menu_type == 1 or menu_type == 3:
            parent_map[parent_id]["menus"].append(menu)
        elif menu_type == 2:
            parent_map[parent_id]["buttons"].append(menu)

    # 2. 递归构建树形结构（核心逻辑）
    def build_tree(current_parent_id: int) -> list[dict]:
        """递归生成菜单树，按钮挂载到父菜单的 meta.authList"""
        tree_nodes = []
        # 获取当前父ID下的所有菜单（按钮不参与递归，仅挂载到菜单的 meta.authList）
        current_menus = parent_map.get(current_parent_id, {}).get("menus", [])

        for menu in current_menus:
            menu_id = menu["id"]
            # 基础菜单节点构建（核心字段）
            menu_node = {
                "id": menu_id,
                "name": menu.get("name", ""),
                "path": menu.get("path", ""),
                "component": menu.get("component", ""),
                "meta": menu.get("meta", {}) or {},  # 继承原meta字段
                "children": []  # 子菜单（仅菜单节点）
            }

            # 关键：构建 meta.authList（当前菜单下的所有按钮）
            menu_buttons = parent_map.get(menu_id, {}).get("buttons", [])
            auth_list = []
            for btn in menu_buttons:
                # 按钮节点标准化（仅保留核心字段）
                auth_list.append({
                    "id": btn["id"],
                    "name": btn.get("name", ""),
                    "authMark": btn.get("auth_mark", ""),
                    "title": btn.get("meta", {}).get("title", ""),  # 安全取值，避免KeyError
                    "type": 2  # 标记为按钮类型（可选）
                })

            # 将 authList 挂载到 meta 下（覆盖/合并原有 authList）
            menu_node["meta"]["authList"] = auth_list

            # 递归挂载子菜单（仅菜单有子节点，按钮无）
            child_menu_tree = build_tree(menu_id)
            if child_menu_tree:
                menu_node["children"] = child_menu_tree

            tree_nodes.append(menu_node)

        return tree_nodes

    # 3. 从顶级菜单（parent_id=0）开始构建
    return build_tree(0)