from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` RENAME COLUMN `status` TO `enabled`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` RENAME COLUMN `enabled` TO `status`;"""


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
    "3rEHfEcAsAv3dgwUIta8OuthxuJwrx3asC52MfKRhVJdjHykHdtYgjtN2b4stS1OobXNw9"
    "dNbYt2FFPbxRcB+QR3JotdTHBnct8vSnCXTP0Q4l103Sd6n2PoOtGOYtcx1mWdxvjV6jRu"
    "IPaBO3orwStdsiEVjdm8IY2ERrchbV3gtXlDynqt7qY0a9PovoodnFHl8X2kycooPplY8U"
    "X0/rcFyDGXtXf7GZvmz9NomqK27qBnGD74uGSubzvsmdo0D1U1THYKeVz5oNcBNrAecNw6"
    "RFcGzeOcSABSnIbRHpwBRVJr1q8MmsepyUODXkcKYMdl7dFzoA4GVf5KNNj8T6LB2j+xvl"
    "PvhesgTS2aZ6pOlCG9SmbVQ7H7H6LdOdkub9Ud4nyr2azuEGfDOa40AdAd39x2fDNNKFU+"
    "vpnJobwoURIvBSWZkqdfSIPS+Q=="
)
