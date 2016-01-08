VERSION = (0, 2, 0)


def get_version(version=VERSION):
    return ".".join(map(str, version))
