from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "email" VARCHAR(255) NOT NULL UNIQUE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_user_email_1b4f1c";
        ALTER TABLE "user" DROP COLUMN "email";"""


MODELS_STATE = (
    "eJztm21v2zYQx7+KwFcZkAWJF7eFURRwHGfN2jhr4m1Fi0KgJdomLJEKSdU2snz3gdSzLH"
    "mRbWXSyncxeSeRP1J3f52YR+BSGzn85ILShQvZAvSMR0Cgi0DP2Og7NgD0vKRHNgg4cZTx"
    "JG014YJBS4CeMYUOR8cGsBG3GPYEpgT0DOI7jmykFhcMk1nS5BP84CNT0BkSc8RAz/j6Ff"
    "gcMXndB58KBL59OzYAJjZaIS775U9vYU4xcuzM+LEtnVS7Kdaearsm4koZyttPTIs6vksS"
    "Y28t5pTE1pgI2TpDBDEokLy8YL6cjxxuOPVoisHQE5NgiCkfG02h74jU/J8JxaJEAsVEyA"
    "k/gpm8y8+ds/PX529+eXX+5tgAaiRxy+unYHrJ3ANHRWA0Bk+qHwoYWCiMCTeF2axEL+3y"
    "7wwjYtsgRg0JxWQrNQljgk3u0mrUUh4/EjT5wE4XhVsvetKzAK8oQ3hGPqC14nhNuIDEQg"
    "XcwpD1R3iZ5vEL4SStSXhgcBkHsfTWoMS0kYOEmuCgfz/oXw5BZucFcXF/bJ+i67SXWzoQ"
    "FYOTu28CrcUSMtvMbEPZQzs01xLbbna5HTffAgmcKQByGnLQIdpLDNm6KLsGHVtTqx2bHD"
    "Sv6jRabxoVWDgFT+VgDlkxu9ghh4+LhgYz4MKV6SAyE3PQM85OT7fw+rN/N3jfvzs6Oz39"
    "ST2cDFrB9h6FXZ2gL5tULUoECrZPFuMYrUq2YMqlLSC3cBsPP4/loF3OH5w0rqOb/mdF0l"
    "2HPR9vR79G5im8g4+3F3mqDMn5m7AA7CUUSGAXlcDNeOb42qHrSfRHXbTB26lPLEnZGFGC"
    "TnxhEbp8B+pZgeub4f24f/N7Zhku++Oh7OlkliBqPXqV2+TxRYy/rsfvDfnT+HI7GiqKlI"
    "sZU3dM7MZfZI4H0BfUJHRpQjuNImqOmjKrS5ekqhJNu2gpmlDUWjS3OZqkqcZ0gciFA62F"
    "g7koElc5i60qS0jbScZWy602yS25flV0QuygVUKxSkArD7OdVELWswEqAXreSRgT5Jv1yV"
    "sHuhMbvtOSQdeudO3qpWtX/41cUGALREIEvFwaRCurBUGbBIFcNfV3hRJM2ucwsqB2ipka"
    "TPc5JZhueQVGdmVFgAc5X1Jmm3PI51VQbji2RWZliXa63Wcg7XS7pUxVX05ZuRA7VWDGDm"
    "3clAdDuJF8yxNJwjr6MM03eV+Erlcf7pAD1SRL03L6K3h7UnNm18nvCBjtySH+XtFSCOqt"
    "z0RE7I9is7rQUiaQczwjyDYffMTlHfYEIxXVp/BSLcNStwCNsZQI0TS27YI0Wqt6D9yE99"
    "BnbmoWq5DwJWLmDp+7Nj130gghr/9xOSsAtVM9K+d6gIJWs3C3rVwVxaWqh9QyXj9S2UrX"
    "+nStrwnn1BLJsvdRtTbKy83TapmI1KRqaXAWsEClxocEy+VpfB5RF0zbpEH1WataZKcv5p"
    "RVKfYlHi1R8jWdA9TlvkaVL7aVLp5XtqivZKFTQ72pIRYqAq0qJYgNR50mkjSxU4CLi7VS"
    "eutCbR2Rro8YtuZFcS7s2RrlYGKjY1yLYtx3xHjhy2m5Uku5tCWuvcDXbfloVJG7gXk7Ab"
    "7sP738dn87qvoiZmNLGH8bjf9EOS3gJ+e7PdPmk2qu2CwvUDHTHj6xPP0DIxB0Vg=="
)
