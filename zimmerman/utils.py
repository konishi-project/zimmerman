def Message(success, message):
    response_object = {
        "success": success,
        "message": message,
    }
    return response_object


def InternalErrResp():
    err = Message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500


def ErrResp(message, reason, code):
    err = Message(False, message)
    err["error_reason"] = reason
    return err, code


def RouteAccessDenied():
    err = Message(False, "You do not have enough permissions to access the route.")
    err["error_reason"] = "access_denied"
    return err, 401
