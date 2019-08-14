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
    message = None

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message


class RequiredParametersMissingException(VOPException):
    code = 422
    name = "RequiredParametersMissingException"
