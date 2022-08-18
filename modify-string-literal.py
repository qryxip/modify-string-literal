#!/usr/bin/env python
import platform
import subprocess
import sys
from ctypes import POINTER, c_char, cdll


def main() -> None:
    subprocess.run(["cargo", "build"], check=True)

    lib1 = cdll.LoadLibrary(f"./target/debug/{dll_name('lib1')}")
    lib1.version_as_heap_allocated_string.argtypes = ()
    lib1.version_as_heap_allocated_string.restype = POINTER(c_char)

    lib2 = cdll.LoadLibrary(f"./target/debug/{dll_name('lib2')}")
    lib2.modify_char.argtypes = (POINTER(c_char),)

    print("Modifying a heap allocated string", file=sys.stderr)
    version = lib1.version_as_heap_allocated_string()
    lib2.modify_char(version)
    print("Modifying a heap allocated string: OK", file=sys.stderr)

    print("Modifying a string literal", file=sys.stderr)
    version = POINTER(c_char).in_dll(lib1, "version_as_string_literal")
    lib2.modify_char(version)
    print("Modifying a string literal: OK", file=sys.stderr)


def dll_name(stem: str) -> str:
    if platform.system() == "Windows":
        return f"{stem}.dll"
    if platform.system() == "Darwin":
        return f"lib{stem}.dylib"
    if platform.system() == "Linux":
        return f"lib{stem}.so"
    raise RuntimeError("unsupported")


if __name__ == "__main__":
    main()
