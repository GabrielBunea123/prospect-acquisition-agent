import uuid


def generate_id() -> str:
    """
    Generate unique id
    :return:
    """
    return str(uuid.uuid4())
