from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pems_web")
except PackageNotFoundError:
    # package is not installed
    pass
