import os
import pathlib

from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
from conan.tools.env import VirtualRunEnv
from conans import ConanFile


class CuraConan(ConanFile):
    name = "Cura"
    version = "4.10.0"
    license = "LGPL-3.0"
    author = "Ultimaker B.V."
    url = "https://github.com/Ultimaker/cura"
    description = "3D printer / slicing GUI built on top of the Uranium framework"
    topics = ("conan", "python", "pyqt5", "qt", "qml", "3d-printing", "slicer")
    settings = "os", "compiler", "build_type", "arch"
    generators = "PyCharmRunEnv", "VirtualRunEnv"
    pycharm_targets = [
        {
            "jinja_path": os.path.join(".conan_gen", "Cura.run.xml.jinja"),
            "name": "Cura",
            "entry_point": "cura_app.py",
            "arguments": ""
        },
        {
            "jinja_path": os.path.join(".conan_gen", "Cura.run.xml.jinja"),
            "name": "CuraExternalEngine",
            "entry_point": "cura_app.py",
            "arguments": "--external"
        }
    ]
    options = {
        "python_version": "ANY",
        "enterprise": [True, False],
        "staging": [True, False],
        "external_engine": [True, False]
    }
    default_options = {
        "python_version": "3.9",
        "enterprise": False,
        "staging": False,
        "external_engine": False
    }
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
        self.options["Arcus"].python_version = self.options.python_version

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
        self.requires(f"Charon/4.10.0@ultimaker/testing")
        self.requires(f"pynest2d/4.10.0@ultimaker/testing")
        self.requires(f"Savitar/4.10.0@ultimaker/testing")
        self.requires(f"Uranium/4.10.0@ultimaker/testing")
        self.requires(f"CuraEngine/4.10.0@ultimaker/testing")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()

    def package_info(self):
        self.runenv_info.define("CURA_APP_DISPLAY_NAME", self.name)
        self.runenv_info.define("CURA_VERSION", "master")
        self.runenv_info.define("CURA_BUILD_TYPE", "Enterprise" if self.options.enterprise else "")
        staging = "-staging" if self.options.staging else ""
        self.runenv_info.define("CURA_CLOUD_API_ROOT", f"https://api{staging}.ultimaker.com")
        self.runenv_info.define("CURA_CLOUD_ACCOUNT_API_ROOT", f"https://account{staging}.ultimaker.com")
        self.runenv_info.define("CURA_DIGITAL_FACTORY_URL", f"https://digitalfactory{staging}.ultimaker.com")
