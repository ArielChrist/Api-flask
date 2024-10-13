from marshmallow import Schema, fields, validate
from .models import RoleEnum

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))
    role = fields.Enum(RoleEnum, by_value=True)

class TagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    author_id = fields.Int(required=True)
    author = fields.Nested(UserSchema(only=('id', 'username')), dump_only=True)
    tags = fields.Nested(TagSchema(many=True))
