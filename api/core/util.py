def convert_menu_to_tree(menu_list):
    """
    将扁平的菜单列表转换为嵌套的树形结构
    :param menu_list: 数据库查询的扁平菜单列表（字典列表）
    :return: 嵌套的菜单树形结构
    """
    # 1. 构建父ID到子菜单的映射（key: parent_id, value: 子菜单列表）
    parent_map = {}
    for menu in menu_list:
        parent_id = menu["parent_id"]
        if parent_id not in parent_map:
            parent_map[parent_id] = []
        parent_map[parent_id].append(menu)

    # 2. 递归构建树形结构
    def build_tree(parent_id):
        """递归生成子菜单树"""
        tree = []
        # 获取当前父ID下的所有子菜单
        children = parent_map.get(parent_id, [])
        for child in children:
            # 基础字段映射
            menu_node = {
                "id": child["id"],
                "name": child["name"],
                "path": child["path"],
                "component": child["component"],
                "meta": child["meta"]
            }
            # 为当前菜单递归挂载子菜单
            child_tree = build_tree(child["id"])
            if child_tree:
                menu_node["children"] = child_tree
            tree.append(menu_node)
        return tree

    # 3. 从顶级菜单（parent_id=0）开始构建
    return build_tree(0)


if __name__ == '__main__':
    pass
