from marshmallow import Schema, fields


class InternalErrorSchema(Schema):
    type = fields.String()
    description = fields.String()


class ErrorSchema(Schema):
    success = fields.String()
    error = fields.Nested(InternalErrorSchema)


class VOPException(Exception):
    code = 500
    name = "VOPException"
    description = None

    def __init__(self, description):
        self.description = description


class RequiredParametersMissingException(VOPException):
    code = 422
    name = "RequiredParametersMissingException"
