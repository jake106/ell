import setuptools
import os

# Read the README.md for the long description
# It's good practice to ensure the file exists and handle potential errors.
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "" # Fallback if README.md is not found

# Core dependencies
# These are packages that are always required for the base functionality of 'ell-ai'.
install_requires = [
    "numpy==2.2.6",
    "dill",
    "colorama",
    "cattrs",
    "openai>=1.51.0",
    "requests",
    "typing-extensions",
    "pillow>=10.4.0",
    "psutil",
]

# Optional dependencies (extras)
# These allow users to install specific subsets of features, e.g., 'ell-ai[anthropic]'
# Version ranges converted from Poetry's caret (^) operator:
# ^A.B.C -> >=A.B.C, <(A+1).0.0 (for A > 0)
# ^0.Y.Z -> >=0.Y.Z, <0.(Y+1).0 (for A == 0)
extras_require = {
    "anthropic": ["anthropic>=0.34.2"],
    "groq": ["groq>=0.11.0"],
    "google": ["google-genai>=1.2.0,<2.0.0"], # Converted from ^1.2.0
    "sqlite": [
        "sqlmodel>=0.0.21,<0.1.0", # Already precise in Poetry
        "alembic>=1.14.0,<2.0.0",  # Converted from ^1.14.0
    ],
    "postgres": [
        "sqlmodel>=0.0.21,<0.1.0", # Already precise in Poetry
        "psycopg2>=2.7",           # Already precise in Poetry
        "alembic>=1.14.0,<2.0.0",  # Converted from ^1.14.0
    ],
    "studio": [
        "fastapi>=0.111.1,<0.112.0", # Converted from ^0.111.1
        "uvicorn>=0.30.3,<0.31.0",   # Converted from ^0.30.3
        "sqlmodel>=0.0.21,<0.1.0",   # Inherited dependency, ensure consistent version
        "alembic>=1.14.0,<2.0.0",    # Inherited dependency, ensure consistent version
    ],
    # Development dependencies are often grouped under a 'dev' extra for easy installation
    # e.g., `pip install -e '.[dev]'` for local development.
    "dev": [
        "pytest",
        "sphinx",
        "sphinx-rtd-theme",
        "black", # Moved from core dependencies as it's typically a dev tool
    ]
}

# The 'all' extra in Poetry combines all optional dependencies.
# We manually combine them here using a set to handle potential duplicates and then sort for consistency.
all_dependencies_set = set()
for extra_deps in extras_require.values():
    all_dependencies_set.update(extra_deps)

# Remove the 'dev' dependencies from 'all' if 'all' is meant for runtime production extras.
# In Poetry's 'all', it usually combines just the *runtime* optional extras.
# Let's ensure 'all' only contains the explicitly listed extras from poetry and not 'dev'.
# Re-evaluate based on poetry's [tool.poetry.extras].
# The "all" extra explicitly lists "anthropic", "groq", "google-genai",
# "sqlmodel", "fastapi", "uvicorn", "alembic".
# This means it pulls dependencies from the providers, studio, and default storage groups.

all_extras_list = [
    "anthropic>=0.34.2",
    "groq>=0.11.0",
    "google-genai>=1.2.0,<2.0.0",
    "sqlmodel>=0.0.21,<0.1.0",
    "alembic>=1.14.0,<2.0.0",
    "fastapi>=0.111.1,<0.112.0",
    "uvicorn>=0.30.3,<0.31.0",
]
extras_require["all"] = sorted(list(set(all_extras_list)))


setuptools.setup(
    name="ell-ai",
    version="0.0.17", # Directly from tool.poetry.version
    author="William Guss", # From tool.poetry.authors (first entry)
    author_email="will@lrsys.xyz", # From tool.poetry.authors (first entry)
    description="ell - the language model programming library", # From tool.poetry.description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jake106/ell", # From tool.poetry.repository
    # project_urls can include other relevant links like documentation, issues, etc.
    project_urls={
        "Homepage": "https://docs.ell.so", # From tool.poetry.homepage
        "Repository": "https://github.com/MadcowD/ell", # Also from tool.poetry.repository
    },
    # packages should use setuptools.find_packages with 'where' to locate packages under 'src'
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"}, # Tells setuptools that packages are in the 'src' directory
    python_requires=">=3.9", # From tool.poetry.dependencies.python
    install_requires=install_requires,
    extras_require=extras_require,
    # include_package_data=True tells Setuptools to look for a MANIFEST.in file
    # for non-code files that should be included in the distribution.
    include_package_data=True,
    classifiers=[ # From tool.poetry.classifiers, adjusted for python_requires
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13", # Including 3.13 if implicitly supported by >=3.9
    ],
    # Console scripts for command-line executables
    entry_points={
        "console_scripts": [
            "ell-studio = ell.studio.__main__:main",
        ],
    },
)
