from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="silentis-ai",
    version="1.0.0",
    author="Silentis Team",
    author_email="support@silentis.ai",
    description="Silentis AI - A powerful AI assistant plugin.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Silentisai/Silentis",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "llama-cpp-python",
        "psutil",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "silentis=silentisai.run:main",  # Allows running as `silentis` command
        ],
    },
)
