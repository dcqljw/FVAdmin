from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `nickname` VARCHAR(255) NOT NULL COMMENT '昵称';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP COLUMN `nickname`;"""


MODELS_STATE = (
    "eJztm21vm0gQgP+K5U85qVdhbMC+b26SU3O6JFXi3p3aVGiBtY0CC4WlqVXlv3d28ZoXYx"
    "+kxBCHL4TMzsDOs28zu/hH3/Us7IRvpziwzWX/j96PPkEuhptcyZteH/l+ImcCigyHq6JE"
    "xwhpgEwK0jlyQgwiC4dmYPvU9ghISeQ4TOiZoGiTRSKKiP01wjr1FpgucQAFn7+A2CYW/o"
    "5D8a9/r89t7FiZqtoWezeX63Tlc9kFoX9yRfY2Qzc9J3JJouyv6NIjG22bUCZdYIIDRDF7"
    "PA0iVn1Wu7WfwqO4polKXMWUjYXnKHJoyt2SDEyPMH5Qm5A7uGBv+V0ejLTReKiOxqDCa7"
    "KRaI+xe4nvsSEncDXrP/JyRFGswTEm3L7hIGRV2oJ3ukRBMb2USQ4hVDyPUADbx1AIEohJ"
    "x6mJoou+6w4mC8o6uKwoe5j9M705fT+9OQGt35g3HnTmuI9frYvkuIyBTUCyoVEB4lr9ZQ"
    "IcSFIJgKC1EyAvywKEN1Icj8EsxL9ur6+KIaZMciA/EnDws2Wb9E3PsUP6pZ1Y91BkXrNK"
    "u2H41UnDO7mc/pfnevr39TtOwQvpIuBP4Q94B4zZlDm/Tw1+JjCQef+AAkvfKvFkb5fudp"
    "Eru3kJImjBWTGPmX/rReQSk6hoceHyvUuLKzS6heUFLSw+CmBo6pXwZWz+n2JdY1jaoti/"
    "izR5qMIVIy2uzqGIJgT53wpLitBveE0BduOhZd5FylBR4DqSLOA4mUslKT7/Uu0juqwCVu"
    "i3C+wY1OF+Ph61BiybqWM85cd8xuZwY74MYc3UDLjXxkYzE4CLKaoSDgn9GmKh9WJT/2ww"
    "GA3vIlXRJLgOVVwO7CHCpGwo6voeKQxGd88SGaPmp4rJWAPeE02VWzlVmAFmIHRUwPgMSq"
    "jt4h2cM5Y50Nba9K24OTR2RR6wOQP0WDefQwgxUeZlsYNn1jVxVusBuIf67OLy/HY2vfyQ"
    "6ftn09k5K5G5dJWTnqi5Bto8pPfvxex9j/3b+3R9dZ4fIhu92ac+qxOKqKcT70FHViowFV"
    "KBK9PckW89sbmzlm1rblWdj1hDG9Irbm5e+cOlmalADgeuHbLNqHC7W10ispp57Mo71gWw"
    "R8QsCjPWmeiHzdOe0oueO197FANDSJNX8Prrubw6602AHT6K0pFazMwLOPR7vMoSXWdhm1"
    "ZZK/BwLS6iy8CLFsucmcjW4RbqgWm8ak5vT6dnvKfp+Tz4ce+2QcqNgs2DrJO7txD8rF63"
    "kVBjx3zujYQXmga3aW/ahBFRLZS1OoRZhOmaVSCZM+uAHncCUB7wscR+ryTUf30N21hQn4"
    "SmvxbOi4Ollx7ICz/yIXw++ckG8qk4PR/Cb8X4NQTy29NA4Dm4jma8geccQzMKP6o1I6P4"
    "hGbkZtmkp6Z8jLtRkIkJ93bnYIHQ6LKvOtebLvtqe6TbpQ41A4UlgxaFCDvHc2LQ8AHjgY"
    "d1l20dWVDeZVtH2rDdEcoBYqV6j1CSBKfiEUoqpq8hZC+YEkIc1NGYH+E5x9CMwo+yDcj4"
    "VWo6biDSm5ryLF7pgjxLOLM7z4qERpdntS4g251nsVarmmulbZr/4EhT5PFdpMpDLf7os9"
    "+WdIHY5n3lNDZl0zxaVR0qrfuGNgwfvKBgtO/7jjaxaR6qYpjsA++xNGgNVOwi26lCdGPQ"
    "PM6JhDDgNIz24PQBSaVRvzFoHqcqjwy4akPEPp2da0+BOhiU+ZXWYPePtAZbP3L7ButXUA"
    "VpYtE8U2UyHMFVMuet6aIvYitrULjcywZMn6pUevrsdrTKddLuA+JXs8/VfUDc8O5Xd0hd"
    "7pA62VIqfTyd2kX5pa2SeCoo2Ct5/AnMG10G"
)
