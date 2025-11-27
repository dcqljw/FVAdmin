from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` ADD UNIQUE INDEX `code` (`code`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` DROP INDEX `code`;"""


MODELS_STATE = (
    "eJztm21vm0gQgP+K5U85KVdhbMC+b26SU3O6JFXi3p3aVGiBxUaBhcLSNKry3zu7eM2LsQ"
    "8SxxCHL4TMzsDus28zw/pn3/Mt7Ebvpjh0zEX/j97PPkEehptCyXGvj4IglTMBRYbLVVGq"
    "Y0Q0RCYFqY3cCIPIwpEZOgF1fAJSErsuE/omKDpknopi4nyLsU79OaYLHELBl68gdoiFf+"
    "BI/Bvc6baDXStXVcdi7+ZynT4EXHZO6J9ckb3N0E3fjT2SKgcPdOGTlbZDKJPOMcEhopg9"
    "noYxqz6r3bKdokVJTVOVpIoZGwvbKHZpprkVGZg+YfygNhFv4Jy95Xd5MNJG46E6GoMKr8"
    "lKoj0mzUvbnhhyApez/iMvRxQlGhxjyu07DiNWpTV4JwsUltPLmBQQQsWLCAWwbQyFIIWY"
    "DpwdUfTQD93FZE7ZAJcVZQuzf6bXJx+m10eg9RtrjQ+DORnjl8siOSljYFOQbGrUgLhUf5"
    "0AB5JUASBobQTIy/IA4Y0UJ3MwD/Gvm6vLcogZkwLITwQa+MVyTHrcc52Ifm0n1i0UWatZ"
    "pb0o+uZm4R1dTP8rcj35++o9p+BHdB7yp/AHvAfGbMm07zKTnwkMZN7do9DS10p82d+ku1"
    "7kyV5Rggiac1asxax9y03kApO4bHPh8q1biyc0uo3lFW0sAQphauq18OVs/p/iruawtEax"
    "fxtr8lCFK0ZaUp19EU0J8r81thSh3/CeAuzGQ8u8jZWhosB1JFnAcWJLFSm+/FYdILqoA1"
    "botwvsGNTh3h6PWgOWrdQJnupzPmezvzlfhbBmagbca2OjmQXAwxTVcYeE/g58oeVms/vV"
    "YDAa3saqoklwHaq4Gth9uEl5V9QLfFLqjG5eJXJGzS8Vk7EGvCeaKrdyqTBDzEDoqITxKZ"
    "RQx8MbOOcsC6Ctpek7cbNv7Io8YGsG6LFhboMLMVHsqtihZdYVcR+WE3AL9dn5xdnNbHrx"
    "MTf2T6ezM1Yic+lDQXqkFjpo9ZDev+ezDz32b+/z1eVZcYqs9Gaf+6xOKKa+Tvx7HVkZx1"
    "RIBa5cd8eB9cTuzlu2rbtV1R6xjjakN9zdvPL7CzMzjhwOPSdiyahofVhdIPIw89mVD6xz"
    "YI+IWeZmLCPRa9990vh56UjtUUwJIU1fwWuuFyJq0Y4Qu3zmZL2zhJMfctB3mA29fgj6y5"
    "hr1QfLIu6cJUV0EfrxfLEyEFE5cIS3YprsjtObk+kpH1F6Md593Joe+Ljqyn5JkiBTerwt"
    "VRDk9bqEwQ6H4UsnDF5puNumHLQJM6Key2p1CPMIszWrQbJg1gE9bEe/OuBD8fHeiEv/9j"
    "p2z877VieQe64l7p/waDc7fqHQ6Fy+zuWruEi8OL1Dd/gOAGDn7u0YaEQRjUuyMRuXw9Sg"
    "4Y8/e14VOw/5wBypzkM+0I5tLL2dJmyfl9gWR6zatr/XTWyLdhQT28XPAPn0diaHXUxvZz"
    "Lfz0pvl0z9CIe76LpP8JxD6DrRjmLXMdZlncb41eo0biCiwB19k+CVLglHRWM2h6Ox0OjC"
    "0dY5XpvDUdZrdUPSrE2jURU7sqjI49tYlYdacuyu4mfolw8KiGPe1Y71MzbNn6ZR1aHSul"
    "OMUXTvhyVzfdtJxtSmeaiKYbIjtmNp0Bqo2EOOW4foyqB5nBMJYcBpGO3BGQCSWrN+ZdA8"
    "TlUeGXDVhogdXrS1p0AdDKr8Tmaw+Wcyg7WfGX2H3SusgzS1aJ6pMhmO4CqZdmuG6KtIWA"
    "1Kt3vZgOVTlSovn13eqtog7Y5wvplsVneEs+EcV5oA6A5vbju8mSaUKh/ezORQnpUoSZaC"
    "kkzJ4y9K3nsq"
)
