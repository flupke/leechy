def force_utf8(value):
    if isinstance(value, unicode):
        return value.encode('utf8')
    return value
