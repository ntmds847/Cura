import os

from conans import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
from conan.tools.env import VirtualRunEnv

class CuraConan(ConanFile):
    name = "Cura"
    version = "4.10.0"
    license = "LGPL-3.0"
    author = "Ultimaker B.V."
    url = "https://github.com/Ultimaker/cura"
    description = "3D printer / slicing GUI built on top of the Uranium framework"
    topics = ("conan", "python", "pyqt5", "qt", "qml", "3d-printing", "slicer")
    settings = "os", "compiler", "build_type", "arch"
    # generators = "virtualenv_ultimaker", "pycharm_run"
    options = {
        "python_version": "ANY"
    }
    default_options = {
        "python_version": "3.9"
    }
    _source_subfolder = "cura-src"

    scm = {
        "type": "git",
        "subfolder": ".",
        "url": "auto",
        "revision": "auto"
    }

    def configure(self):
        self.options["Charon"].python_version = self.options.python_version
        self.options["Savitar"].python_version = self.options.python_version
        self.options["Uranium"].python_version = self.options.python_version
        self.options["pynest2d"].python_version = self.options.python_version

    def build_requirements(self):
        self.build_requires("cmake/[>=3.16.2]")

    def generate(self):
        rv = VirtualRunEnv(self)
        rv.generate()

        cmake = CMakeDeps(self)
        cmake.generate()

        tc = CMakeToolchain(self)
        tc.variables["Python_VERSION"] = self.options.python_version
        tc.variables["URANIUM_CMAKE_PATH"] = self.deps_user_info["Uranium"].URANIUM_CMAKE_PATH
        tc.generate()

    def requirements(self):
        # self.requires("virtualenv_ultimaker_gen/0.1@ultimaker/testing")
        # self.requires("pycharm_run_gen/0.1@ultimaker/testing")
        self.requires(f"Charon/4.10.0@ultimaker/testing")
        self.requires(f"pynest2d/4.10.0@ultimaker/testing")
        self.requires(f"Savitar/4.10.0@ultimaker/testing")
        self.requires(f"Uranium/4.10.0@ultimaker/testing")
        # self.requires(f"CuraEngine/4.10.0@ultimaker/testing")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()