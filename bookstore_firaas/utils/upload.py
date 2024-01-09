import os
import uuid
from functools import partial


def _update_filename(instance, filename, path):
    path = path

    splitFilename = os.path.splitext(filename)

    filename = str(uuid.uuid4()) + splitFilename[len(splitFilename) - 1]

    return os.path.join(path, filename)


def upload_to(path):
    return partial(_update_filename, path=path)
