VERSION = (0, 1, 5)


def get_version(version=VERSION):
    return ".".join(map(str, version))
