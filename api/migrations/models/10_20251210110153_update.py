from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `menu` ADD `sort` INT NOT NULL COMMENT '排序' DEFAULT 0;
        ALTER TABLE `menu` ADD `status` INT NOT NULL COMMENT '状态' DEFAULT 1;
        ALTER TABLE `menu` DROP COLUMN `menu_type`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `menu` ADD `menu_type` INT NOT NULL COMMENT '菜单类型';
        ALTER TABLE `menu` DROP COLUMN `sort`;
        ALTER TABLE `menu` DROP COLUMN `status`;"""


MODELS_STATE = (
    "eJztm21zmzgQgP+Kx59yM7kOBoPt++YmuWluLkknce9u2nQYAcJmDIIK0TTTyX+vJJB5Mf"
    "ZBYhvi8AXbq12QHr3sapF/9j3fgm74bgqxYy76f/R+9hHwIP1SKDnt9UEQpHImIMBwuSpI"
    "dYyQYGASKrWBG0IqsmBoYicgjo+oFEWuy4S+SRUdNE9FEXK+RVAn/hySBcS04MtXKnaQBX"
    "/AUPwMlrrtQNfKVdWx2LO5XCePAZddIvInV2RPM3TTdyMPpcrBI1n4aKXtIMKkc4ggBgSy"
    "2xMcseqz2iXtFC2Ka5qqxFXM2FjQBpFLMs2tyMD0EeNHaxPyBs7ZU36XB8PRcKxowzFV4T"
    "VZSUZPcfPStseGnMD1rP/EywEBsQbHmHL7DnHIqrQG72wBcDm9jEkBIa14EaEAto2hEKQQ"
    "04GzI4oe+KG7EM0JG+Cyqm5h9s/09uzD9PaEav3GWuPTwRyP8eukSI7LGNgUJJsaNSAm6q"
    "8T4ECSKgCkWhsB8rI8QPpEAuM5mIf4193NdTnEjEkB5CdEG/jFckxy2nOdkHxtJ9YtFFmr"
    "WaW9MPzmZuGdXE3/K3I9+/vmPafgh2SO+V34Dd5TxmzJtJeZyc8EBjCXDwBb+lqJL/ubdN"
    "eLPNkrSgACc86KtZi1L3EiVxBFZc6Fy7e6Fk9odI7lFTmWAGA6NfVa+HI2/09xV3NYWqPY"
    "v49GsqLRKwSjuDqHIpoS5J81XIrQb9inUHZjxTLvI1VRVXodShblOLGlihT376oDQBZ1wA"
    "r9doEdU3X63R4PWwPWgwTU8d9CfwfOO1kddz98B0PlPtLUkUSvigarsT6EX8+CD31cEjht"
    "XGeFesNLrKZMZEoYju1mFtiQABKFdbitDA5HblDunAzqnDRJGjRDzvS9wEel0frmZTRn1P"
    "xaOhmP6PyejDS5lWupiSEDoYMSxue0hDge3MA5Z1kAbSWm78SXQ2NX5YHBJr0N2LJq02E8"
    "Ue2q2GnLrBvkPiYL/hbqs8uri7vZ9Opjbq09n84uWInMpY8F6YlW6KDVTXr/Xs4+9NjP3u"
    "eb64vikrzSm33uszqBiPg68h90YGUidyEVuHLdHQXWM7s7b9m27tY0e8g62pDecHfzyh9u"
    "H56JdCH2nJBl60rc3BVAjzOfXfnAuqTsATLLthDJVv3Wd581fva9lX0SU0JI00fwmuuFlI"
    "NoB4Yunzlp+IqScMDHHPQSsqHXx1Q/2ZSu+iApYiZJEVlgP5ovVgYibUE50qdCEnvH6d3Z"
    "9JyPKL2YEHjamj/5uOrKfkkWJVN6ui2XEuT1uozKDofhvjMqrzQf0KYkvUlnRL2Q1eoQ5h"
    "Fma1aDZMGsA3rcgX51wMcS472RkP7tdeyBg/etQSCPXEvCPxHRbg78sNDoQr4u5Ku4SOyd"
    "3rEHfEcAsAv3dgz0Vbx0aMOq2EXIRxZIdRHykXZsY+ntNGH7ssS2OIPWNv9eN7Et2lFMbB"
    "dfA+TT25kcdjG9ncl8vyi9XTL1Q4h30XWf6H2OoetEO4pdx1iXdRrjV6vTuIHYBe7onQSv"
    "dMl2VDRm83Y0EhrddrR1gdfm7Sjrtbpb0qxNo7sqdmxGlcf3kSYro/hcYsXX0PvfFCDHXN"
    "be62dsmj9No2mK2rpjnmH44OOSub7tqGdq0zxU1TDZGeRx5WNe+4cKPeC4dYiuDJrHOZEA"
    "pDgNoz04A4qk1qxfGTSPU5OHBr2OFMAOy9qj50AdDKr8kWiw+X9Eg7X/YX2n3gvXQZpaNM"
    "9UnShDepXMqkdiu4RVi0/JHmPeqjvC+aayWd0RzoZzXGkCoDu8ue3wZppQqnx4M5NDeVGi"
    "JF4KSjIlT78AS0vSqw=="
)
