from setuptools import find_packages, setup

setup(
    name="gh0sty",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.7.0",
        "requests>=2.31.0",
        "httpx>=0.27.0",
        "dnspython>=2.6.1",
    ],
    entry_points={
        "console_scripts": [
            "gh0sty=gh0sty.cli:main",
        ],
    },
)
