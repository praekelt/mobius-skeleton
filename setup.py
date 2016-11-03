from setuptools import setup, find_packages


def get_long_description():
    description = ""
    for name in ("README.rst", "AUTHORS.rst", "CHANGELOG.rst"):
        try:
            fp = open(name, "r")
            description += fp.read()
        except IOError:
            pass
        finally:
            fp.close()
    return description


setup(
    name="mobius-skeleton",
    version="0.1",
    description="Create a Mobius project environment quickly.",
    long_description = get_long_description(),
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="",
    packages = find_packages(),
    install_requires = [
        # Handled by requirements file
    ],
    include_package_data=True,
    tests_require=[
        "tox"
    ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
