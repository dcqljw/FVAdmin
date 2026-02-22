from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "llmmodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "baseUrl" TEXT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "apiKey" VARCHAR(100) NOT NULL
);
        ALTER TABLE "user" ALTER COLUMN "avatar" SET DEFAULT '';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "avatar" DROP DEFAULT;
        DROP TABLE IF EXISTS "llmmodel";"""


MODELS_STATE = (
    "eJztm21zozYQgP+Kx5/SmfQGYwN2vzkv7aWN45vEaW8uyTACZJsJCA7EJZlr/nslYfFmoJ"
    "D4PXxxHGnXSI9W2tV6/bNtOwa0/E9D6Jn6vP1b62cbARuSN5me41YbuG7cThsw0CwmCmIZ"
    "zcce0DFpnQLLh6TJgL7umS42HURaUWBZtNHRiaCJZnFTgMzvAVSxM4N4Dj3ScfdAmk1kwG"
    "fo83/dR3VqQstIDdU06LNZu4pfXNZ2gfDvTJA+TVN1xwpsFAu7L3juoEjaRJi2ziCCHsCQ"
    "fjz2Ajp8OrrFPPmMwpHGIuEQEzoGnILAwonpVmSgO4jyI6Px2QRn9Cm/ip2e0ut35V6fiL"
    "CRRC3Kazi9eO6hIiNwNWm/sn6AQSjBMMbcfkDPp0Nagnc6B14+vYRKBiEZeBYhB1bGkDfE"
    "EGPDWRFFGzyrFkQzTA1clKQSZn8Pr08/D6+PiNQvdDYOMebQxq8WXWLYR8HGIOnWqAFxIb"
    "6fADuCUAEgkSoEyPrSAMkTMQz3YBrinzfjq3yICZUMyFtEJnhnmDo+blmmjx92E2sJRTpr"
    "Omjb979bSXhHo+HXLNfTy/EJo+D4eOaxT2EfcEIY0yNz+pjY/LRBA/rjE/AMdanHEZ0i2e"
    "UuW7SzLQCBGWNFZ0znt3Ail5ejEX2X52CivlIXY1m2HUk1TmaPnIwGfHjrWcvwJvC5gF5C"
    "ZV/OyBJEk/Ovk/LNbL8sei7HV39w8ewOTx+Y7G8Nl8Pl94XnBnwOcM2/4Es9v801PjjGHX"
    "ErI4iCPJfC2kvdic0lGleyR67EBR6J+NRa+FI6/09xVdtWWKLYvg8UsSuTVwiUcDibIrr3"
    "boOw63cN/T6QupJEXnuCQTgOpsK/94HcFQb3waAHYLKjIt71Xw0ZsurmysU3Z6mdXEvVFY"
    "3gVPpaq5NkLyZ5b8eEXYDndUyYy++WCfeJOHk/7fd2xlJBgOeqDbzHWiFRUmn7iJOHgaz0"
    "uuS9LAnkfV9QCHRNl3cGtw0xqJPv4PIrSHYs3P7qz+UOJS5LCiXelSseEJvIgyTB+46Xk2"
    "gqPJG5+JZjB7k7IIevBPvT7Ry7PgY48Je5nTiOBQEqYBcpZehpRGtd+KKgdin60kj0JQtC"
    "5912eTIeX6bs8uQie2e/HZ2ck7sUM1IiZGKYz1V3bNdBubnP4lM3pbT9U3fQV8juHyiyuJ"
    "OOTfcgBaGCHMZnpAebNizgnNLMgDYWqp/4m01jl8QODdKIHD10p8S4B9K0KnYyM2OMrJfF"
    "hinLX12Mzm8mw9GXlMWfDSfntEdMJbB465GcWaDoQ1r/XEw+t+i/rW/jq/PsgR3JTb616Z"
    "hIfOGoyHlSgZG4sPJWjiu13IFrvHG505q7ttyyPO3RhdaED7zcbPCbSz8lwzWU5/5GAL1M"
    "HPrKTOqCUAdIz7vCLXJT18RdvsVy1p27eeWbgbfGj2AjVzM5Nj4PD1pszyxzcjyG+BFSo2"
    "t7RH6RhYnoL7qoyqILzz0nmM0jBZ6nIxzJU2HoRE+HN6fDM2ZLajYD9lqaMPwCPdv0/RDN"
    "Utow0Xtcljx003JNCnGFZrjuFOKeJsB2qdhBJzuiXrBqNAjTCJMjq0Eyo9YAPewQvzrgQ4"
    "nuPkgw//EWdsNhe2kQyCLXnPCPR7TFgZ/HJZqQrwn5Kh4Sa6d36AHfAQBswr0VA4WITi/n"
    "PCz9NiKhtcGvI9ZWV7jKLyGa8PkQoqwmfD7Qhd37rDevyNw15183683nUTXrnUhtZ7PeiY"
    "T4u7LeOZveh94qFu2WfM4hLBqfR3bRKOu8RaP8ai0aU+CXwxV9VcEGnXNL5ZMpvqUGXGKd"
    "t9Q79hg2tofmxnq82htrhHaJXvFlIamz1YsXrbSRxP59IItdJSzJrfgd9frvDcjUH2unAx"
    "I62y+1keWutGMVzi7w/SfHy9nrZUW5sc72oUqaTuvy+1UrwzZxw7WBmfObuWKikcL2cQ4E"
    "Wn6raNru4HQJklq7PlLYPk5Z7Gm0mrkLaJ3tVHkL1E6nyg+/OsW/++osVYv/IN7Lq4M01t"
    "gc03Y7d78Puj3yKuhVa2nXb6BF5bXFZclFpbUb/6lIzbLaVRcmH2Tuqqnu/FAZraa6c8t5"
    "rjgV0FR3llV3xqmlytWdiWzKu1Im4VGQkzN5/Q8PLcq3"
)
