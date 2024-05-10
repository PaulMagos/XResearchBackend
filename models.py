from tortoise import fields, models

class Tweets(models.Model):
    index = fields.IntField()
    type = fields.CharField(max_length=25)
    lang = fields.CharField(max_length=25)
    value = fields.IntField()
    created_at = fields.DateField()

class Words(models.Model):
    id = fields.IntField(pk=True)
    word = fields.TextField()
    lang = fields.CharField(max_length=25)
    frequency = fields.IntField()
    created_at = fields.DateField()
    