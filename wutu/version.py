VERSION = (0, 1, 4)


def get_version(version=VERSION):
    return ".".join(map(lambda x: str(x), version))
