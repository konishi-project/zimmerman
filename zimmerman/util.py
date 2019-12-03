def Message(success, message):
    response_object = {
        "success": success,
        "message": message,
    }
    return response_object


def ErrResp():
    err = Message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500
