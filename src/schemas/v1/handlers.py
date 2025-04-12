def handle_form_str(value):
    if value in ('', None):
        return None
    return value


def handle_form_bool(value):
    if isinstance(value, str):
        lowered = value.lower().strip()
        if lowered in ('true', '1'):
            return True
        elif lowered in ('false', '0'):
            return False
    return None


def handle_form_int(value):
    if value in ('', None) and not value.isdigit():
        return None
    return int(value)


def handle_file(value):
    if hasattr(value, 'filename') and not value.filename:
        return None
    if isinstance(value, str) and not value.strip():
        return None
    return value
