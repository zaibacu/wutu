VERSION = (0, 0, 2)


def get_version(version=VERSION):
	return ".".join(map(lambda x: str(x), version))
