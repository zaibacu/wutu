VERSION = (0, 1, 0)


def get_version(version=VERSION):
    return ".".join(map(lambda x: str(x), version))
