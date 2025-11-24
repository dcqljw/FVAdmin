from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `menu` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `parent_id` INT NOT NULL COMMENT '父级id' DEFAULT 0,
    `name` VARCHAR(255) NOT NULL COMMENT '菜单名称',
    `path` VARCHAR(255) NOT NULL COMMENT '菜单路径',
    `menu_type` INT NOT NULL COMMENT '菜单类型',
    `meta` JSON COMMENT '菜单元数据',
    `component` VARCHAR(255) NOT NULL COMMENT '页面路径',
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间'
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `permission` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `code` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `role` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `status` INT NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '密码',
    `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
    `phone` VARCHAR(11) NOT NULL COMMENT '手机号',
    `avatar` VARCHAR(255) NOT NULL COMMENT '头像',
    `status` INT NOT NULL COMMENT '状态' DEFAULT 1,
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间'
) CHARACTER SET utf8mb4;
        CREATE TABLE `permission_menu` (
    `menu_id` INT NOT NULL REFERENCES `menu` (`id`) ON DELETE CASCADE,
    `permission_id` INT NOT NULL REFERENCES `permission` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE `role_permission` (
    `role_id` INT NOT NULL REFERENCES `role` (`id`) ON DELETE CASCADE,
    `permission_id` INT NOT NULL REFERENCES `permission` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE `user_role` (
    `user_id` INT NOT NULL REFERENCES `user` (`id`) ON DELETE CASCADE,
    `role_id` INT NOT NULL REFERENCES `role` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `role_permission`;
        DROP TABLE IF EXISTS `user_role`;
        DROP TABLE IF EXISTS `role`;
        DROP TABLE IF EXISTS `permission_menu`;
        DROP TABLE IF EXISTS `menu`;
        DROP TABLE IF EXISTS `permission`;
        DROP TABLE IF EXISTS `user`;"""


MODELS_STATE = (
    "eJztm21vm0gQgP+K5U85qVdhbMC+b26SU3O6JFXi3p3aVGiBxUbhrcvS1Kr832928ZoXYx"
    "+kxMY5vhBndgbvPLMvMwv+0fcCC7vR2ykmjrno/9b70feRh+FDoeVNr4/CMJUzAUWGy1VR"
    "qmNElCCTgtRGboRBZOHIJE5IncAHqR+7LhMGJig6/jwVxb7zNcY6DeaYLjCBhs9fQOz4Fv"
    "6OI/Fv+KjbDnatXFcdi303l+t0GXLZlU9/54rs2wzdDNzY81PlcEkXgb/RdnzKpHPsY4Io"
    "ZrenJGbdZ71b+yk8SnqaqiRdzNhY2EaxSzPuVmRgBj7jB72JuINz9i2/yoORNhoP1dEYVH"
    "hPNhJtlbiX+p4YcgI3s/6KtyOKEg2OMeX2DZOIdWkL3vkCkXJ6GZMCQuh4EaEAto+hEKQQ"
    "04HTEEUPfddd7M8pG+Cyouxh9tf07vz99O4MtH5h3gQwmJMxfrNukpM2BjYFyaZGDYhr9d"
    "MEOJCkCgBBaydA3pYHCN9IcTIH8xD/uL+9KYeYMSmA/OiDg58tx6Rveq4T0S/txLqHIvOa"
    "ddqLoq9uFt7Z9fSfItfzP2/fcQpBROeE34Xf4B0wZkum/ZiZ/ExgIPPxCRFL32oJ5GCX7n"
    "aTJ3tFCfLRnLNiHjP/1pvINfbjss2Fy/duLZ7Q6DaWE9pYQkRgauq18OVs/ptiU3NY2qLY"
    "f4g1eajCFSMt6c6hiKYE+d8aW4rQP/KeAuzGQ8t8iJWhosB1JFnAcWJLFSm+/FYdIrqoA1"
    "botwvsGNThsz0etQYsW6kTPNXnfM7mcHO+CmHN1Az4rI2N4ywAHqaoTjok9BvIhdabTfOr"
    "wWA0fIhVRZPgOlRxNbCHSJPyqagXBn5pMrp7lcgZHX+pmIw14D3RVLmVS4VJMAOhoxLGF9"
    "BCHQ/v4JyzLIC21qZvxYdDY1fkAVszQI8NcxtSiIliV8UOnlm3vrtcT8A91GdX15f3s+n1"
    "h9zYv5jOLlmLzKXLgvRMLQRoc5Pe31ez9z32b+/T7c1lcYps9Gaf+qxPKKaB7gdPOrIyia"
    "mQCly5cMeh9cxw5y3bFm5VtUcs0IZUP9wnEl4BYyu+hyssM6kbJp4TseOnaHsgXSN/OQvY"
    "lQ+lK6CNfLMssVjXnh82d3vOuHnpCm0lpoKQpl/B+68XKum8NwS7fN5kc7OEWUA49Ee8zB"
    "Nd112bqKwVeIKWNNEFCeL5omAm6nP4CP3ANNknp/fn0ws+1vRi5bvae1CQcaPkuCDv5O5D"
    "gzCv1x0dNDgwX/ro4EQL3zadRpswI+olr1aHMI8w27MaJAtmHdDXnfJXB9wl9yeV3DfxDK"
    "dNgWxVGp8moz+XwIuHR6eeugs/ikl7sdzJp+6ZzLyYtG9l9Q2k7tsTnwQubiKMd3Cf1xBG"
    "4Ue9MDKKzwgjN8uXOQ1VYNyNktpLuLe76iJCo6u3mkwdunqr7bltVyw0DBS2DFqWIuycz6"
    "nBkR8iHnhad/VVV1919dXxA9mq+qp7TPLcxyRpSVPzMUkmi28gSS9ZBCJMmgjmR7jPawij"
    "8KNqABm/WqHjBqKgaaiy4p0uqayEM7srq1hodJVV61Kw3ZUVi1rd6iprc/zXiDRFHj/Eqj"
    "zUklc5+20pEEIURU8BKRmY+17kTG2Oj1YxTPaG8VgatAYq9pDj1iG6MTg+zomEMOA0jPbg"
    "DAFJrbm/MTg+TlUeGXDVhoi9u2lrz4E6GFT5mdBg96+EBlu/svoGSy2pgzS1OD5TZTIcwV"
    "Uy7dYM0ZM4ZxmU7kyyAcunKlVePrvjlmqDtHuD9X9zCNO9wXrwo5numWm1Z6bpeUflp6WZ"
    "Ev+n6vh0cBQK+dW/jAvdkA=="
)
