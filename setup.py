"""Package metadata for the PokerSkill agent.

Every module of ``pokerskill_agent`` ships as a compiled CPython extension
built for CPython 3.12 on x86-64 Linux; the package is not portable to other
interpreter versions. See README.md.
"""
from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pokerskill-agent",
    version="3.0.0",
    description="PokerSkill: LLMs Can Play Expert-Level Poker without Training or Solvers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Boning Li, Baoxiang Wang, Longbo Huang",
    author_email="li-bn22@mails.tsinghua.edu.cn",
    url="https://github.com/lbn187/PokerSkill",
    python_requires=">=3.12,<3.13",
    packages=find_packages(),
    package_data={
        "pokerskill_agent": ["*.so", "examples/*.json"],
    },
    install_requires=[
        "openai>=1.0,<3.0",
        "httpx>=0.24",
        "requests>=2.28",
        "treys>=0.1",
    ],
    entry_points={
        "console_scripts": [
            "pokerskill-agent=pokerskill_agent.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: Other/Proprietary License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: POSIX :: Linux",
    ],
    zip_safe=False,
)
