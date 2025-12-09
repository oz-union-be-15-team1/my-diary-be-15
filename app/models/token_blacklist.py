from tortoise import fields, models

class TokenBlacklist(models.Model):
    id = fields.IntField(pk=True)
    token = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="blacklisted_tokens")
    expired_at = fields.DatetimeField(null=True)
