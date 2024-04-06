import importlib
import os
import pkgutil


def discover_blueprints():
    """Discovers modules in the app.blueprints namespace,

    Each module should contain a single Blueprint assigned to
    the `blueprint` variable.
    """
    module_paths = [os.path.dirname(__file__)]
    pkgs = pkgutil.iter_modules(module_paths, __name__ + ".")
    for finder, name, is_pkg in pkgs:
        print(f"Found package: {name}")
        module = importlib.import_module(name)
        if hasattr(module, "blueprint"):
            print(f"Registering blueprint: {name}")
            yield module.blueprint


__all__ = ["discover_blueprints"]
