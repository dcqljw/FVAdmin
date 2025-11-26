from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `role_permission`;
        CREATE TABLE `role_menu` (
    `role_id` INT NOT NULL REFERENCES `role` (`id`) ON DELETE CASCADE,
    `menu_id` INT NOT NULL REFERENCES `menu` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `role_menu`;
        CREATE TABLE `role_permission` (
    `role_id` INT NOT NULL REFERENCES `role` (`id`) ON DELETE CASCADE,
    `permission_id` INT NOT NULL REFERENCES `permission` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE `permission_menu` (
    `permission_id` INT NOT NULL REFERENCES `permission` (`id`) ON DELETE CASCADE,
    `menu_id` INT NOT NULL REFERENCES `menu` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


MODELS_STATE = (
    "eJztm19zmzgQwL+Kx0+5mVwHYwP2vblJbpqbS9JJ3LubNh1GgLCZgKAgmno6+e5dCcv8Mf"
    "ZB4hiS8ILxahekn7TSai3/7Hu+hd3o3RSHjrno/9H72SfIw3BTKDnu9VEQpHImoMhwuSpK"
    "dYyIhsikILWRG2EQWTgyQyegjk9ASmLXZULfBEWHzFNRTJxvMdapP8d0gUMo+PIVxA6x8A"
    "8cia/BnW472LVyVXUs9m4u1+ky4LJzQv/kiuxthm76buyRVDlY0oVP1toOoUw6xwSHiGL2"
    "eBrGrPqsdqt2ihYlNU1VkipmbCxso9ilmeZWZGD6hPGD2kS8gXP2lt/lwUgbjYfqaAwqvC"
    "ZrifaQNC9te2LICVzO+g+8HFGUaHCMKbfvOIxYlTbgnSxQWE4vY1JACBUvIhTAdjEUghRi"
    "OnD2RNFDP3QXkzllA1xWlB3M/plen3yYXh+B1m+sNT4M5mSMX66K5KSMgU1BMteoAXGl/j"
    "IBDiSpAkDQ2gqQl+UBwhspTnwwD/Gvm6vLcogZkwLITwQa+MVyTHrcc52Ifm0n1h0UWatZ"
    "pb0o+uZm4R1dTP8rcj35++o9p+BHdB7yp/AHvAfGbMq07zLOzwQGMu/uUWjpGyW+7G/T3S"
    "zyZK8oQQTNOSvWYta+1SJygUlctrhw+c6lxRMa3cLyghaWAIXgmnotfDmb/6e4Lx+WNij2"
    "b2NNHqpwxUhLqnMooilB/lljSRH6Da8pwG48tMzbWBkqClxHkgUcJ7ZUkeLzL9UBoos6YI"
    "V+u8COQR3u7fGoNWDZTJ3gqe7zOZvD+XwVwpqpGXCvjY1mJgAPU1QnHBL6e4iFVovN/meD"
    "wWh4G6uKJsF1qOJqYA8RJuVDUS/wSWkwun2WyBk1P1VMxhrwnmiq3MqpwgwxA6GjEsanUE"
    "IdD2/hnLMsgLZWpu/EzaGxK/KAzRmgx4a5DSHERLGrYoeWWVfEXa4ccAf12fnF2c1sevEx"
    "N/ZPp7MzViJz6bIgPVILHbR+SO/f89mHHvva+3x1eVZ0kbXe7HOf1QnF1NeJf68jKxOYCq"
    "nAlevuOLAe2d15y7Z1t6raI9bRhvSGu5tX/nDbzEwgh0PPiVgyKtocVheILGc+u/KBdQ7s"
    "ETHLwozVTvTadx81fp57p/YgXEJI01fwmuuFHbVoR4hd7jnZ6Czh5Icc9B1mQ68fgv5qz7"
    "Xug1URD86SIroI/Xi+WBuIXTlwhLdimqyO05uT6SkfUXpxv/uwMz3wcd2V/ZIkQab0eFeq"
    "IMjrdQmDPQ7D504YvNDtbpty0CZ4RL2Q1eoQ5hFma1aDZMGsA/q6A/3qgF9LjPdGQvq317"
    "EHDt53BoE8ci0J/0REuz3wC4VGF/J1IV/FSeLZ6XXRyouLViKKaFySTNjqzalBw79dHNip"
    "uwDvlcUBXYD3Sju2sexsmm98Wl5WnBBq2/peNy8r2lHMyxaz2PnsbCYFW8zOZhK3T8rOlr"
    "h+hMN9dN0neM5r6DrRjmLXMdZlncb41eo0biA2MXtKqfNKl+ymRGO276ZiodHtploXeG3f"
    "TbFeq7ujyto0uqtiJ+4UeXwbq/JQS06NVfwV9fk3BcQx72pvVTM2zR8GUdWh0rpDeFF074"
    "clvr7rIF5q0zxUxTDZCdGxNGgNVOwhx61DdG3QPM6JhDDgNIz24AwASS2vXxs0j1OVRwZc"
    "tSFiZ+9s7TFQB4Mqf/MYbP+Xx2DjXzLfYfUK6yBNLZpnqkyGI7hKpt2aIfoiElaD0uVeNm"
    "D6VKXK02eXt6o2SLsTiG8mm9WdQGw4x5UmALqzh7vOHqYJpcpnDzM5lCclSpKpoCRT8vAL"
    "FPwVzA=="
)
