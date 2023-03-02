import os
import subprocess
from contextlib import contextmanager
from pathlib import Path
import os
@contextmanager
def set_directory(path: Path):
    """Sets the cwd within the context
    Args:
        path (Path): The path to the cwd
    Yields:
        None
    """
    origin = Path().absolute()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(origin)
if __name__ == "__main__":
    for dir in os.listdir("."):
        print(dir)
        try:
            os.remove(os.path.join(dir, "security_group.zip"))
        except FileNotFoundError:
            pass
        except NotADirectoryError:
            pass
        if os.path.exists(os.path.join(dir, "security_group")):
            with set_directory(Path(dir)):
                subprocess.run([ "zip", "-r", "security_group.zip", "security_group"], stdout=subprocess.PIPE)
