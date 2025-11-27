from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` ADD `code` VARCHAR(255) NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` DROP COLUMN `code`;"""


MODELS_STATE = (
    "eJztm21vm0gQgP+K5U85KVdhbMC+b26SU3O6JFXi3p3aVGiBxUaBhcLS1Kry3zu7eM2LsQ"
    "8Sx5CEL4TMzsDus28zw/pn3/Mt7Ebvpjh0zEX/j97PPkEehptCyXGvj4IglTMBRYbLVVGq"
    "Y0Q0RCYFqY3cCIPIwpEZOgF1fAJSErsuE/omKDpknopi4nyLsU79OaYLHELBl68gdoiFf+"
    "BI/Bvc6baDXStXVcdi7+ZynS4DLjsn9E+uyN5m6Kbvxh5JlYMlXfhkre0QyqRzTHCIKGaP"
    "p2HMqs9qt2qnaFFS01QlqWLGxsI2il2aaW5FBqZPGD+oTcQbOGdv+V0ejLTReKiOxqDCa7"
    "KWaA9J89K2J4acwOWs/8DLEUWJBseYcvuOw4hVaQPeyQKF5fQyJgWEUPEiQgFsF0MhSCGm"
    "A2dPFD30Q3cxmVM2wGVF2cHsn+n1yYfp9RFo/cZa48NgTsb45apITsoY2BQkmxo1IK7UXy"
    "bAgSRVAAhaWwHysjxAeCPFyRzMQ/zr5uqyHGLGpADyE4EGfrEckx73XCeiX9uJdQdF1mpW"
    "aS+KvrlZeEcX0/+KXE/+vnrPKfgRnYf8KfwB74ExWzLtu8zkZwIDmXf3KLT0jRJf9rfpbh"
    "Z5sleUIILmnBVrMWvfahO5wCQu21y4fOfW4gmNbmN5QRtLgEKYmnotfDmb/6e4rzksbVDs"
    "38aaPFThipGWVOdQRFOC/G+NLUXoN7ynALvx0DJvY2WoKHAdSRZwnNhSRYrPv1UHiC7qgB"
    "X67QI7BnW4t8ej1oBlK3WCp/qcz9kcbs5XIayZmgH32thoZgHwMEV13CGhvwdfaLXZ7H81"
    "GIyGt7GqaBJchyquBvYQblLeFfUCn5Q6o9tXiZxR80vFZKwB74mmyq1cKswQMxA6KmF8Ci"
    "XU8fAWzjnLAmhrZfpO3BwauyIP2JoBemyY2+BCTBS7KnZomXVF3OVqAu6gPju/OLuZTS8+"
    "5sb+6XR2xkpkLl0WpEdqoYPWD+n9ez770GP/9j5fXZ4Vp8hab/a5z+qEYurrxL/XkZVxTI"
    "VU4Mp1dxxYj+zuvGXbultV7RHraEN6w93NK3+4MDPjyOHQcyKWjIo2h9UFIsuZz658YJ0D"
    "e0TMMjdjFYle++6jxs9zR2oPYkoIafoKXnO9EFGLdoTY5TMn650lnPyQg77DbOj1Q9BfxV"
    "zrPlgVcecsKaKL0I/ni7WBiMqBI7wV02R3nN6cTE/5iNKL8e7DzvTAx3VX9kuSBJnS412p"
    "giCv1yUM9jgMnzth8ELD3TbloE2YEfVcVqtDmEeYrVkNkgWzDujrdvSrA34tPt4bcenfXs"
    "ce2Hnf6QRyz7XE/RMe7XbHLxQancvXuXwVF4lnp9c5fC8AYefw7RloRBGNS/IxWxfE1KDh"
    "zz8HXhc7H/mVuVKdj/xKO7axBHeasn1aalscsmqbi1Q3tS3aUUxtFz8E5BPcmSx2McGdyX"
    "0/KcFdMvUjHO6j6z7Bc15D14l2FLuOsS7rNMavVqdxAxEH7umrBK90SUAqGrM9II2FRheQ"
    "ts7x2h6Qsl6rG5RmbRoNTNmhRUUe38aqPNSSg3cVP0Q/f1BAHPOudrSfsWn+PI2qDpXWnW"
    "OMons/LJnru84ypjbNQ1UMkx2yHUuD1kDFHnLcOkTXBs3jnEgIA07DaA/OAJDUmvVrg+Zx"
    "qvLIgKs2ROz4oq09BupgUOWXMoPtP5QZbPzQ6DvsXmEdpKlF80yVyXAEV8m0WzNEX0TCal"
    "C63csGLJ+qVHn57PJW1QZpd4jzzWSzukOcDee40gRAd3xz1/HNNKFU+fhmJofypERJshSU"
    "ZEoefgHBOnvA"
)
