from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="silentis-ai",
    version="1.2.3",
    author="Silentis Team",
    author_email="support@silentis.ai",
    description="Silentis AI - A powerful AI assistant plugin.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Silentisai/Silentis",
    packages=find_packages(),  # Auto-finds "silentis" (if it has __init__.py)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask",
        "requests",
        "llama-cpp-python",
        "psutil",
        "flask-cors",
    ],
    include_package_data=True,  # Respects MANIFEST.in
    package_data={
        "silentis": ["silentis.html"],  # EXPLICITLY include this file
    },
    entry_points={
        "console_scripts": [
            "silentis=silentisai.run:main",  # Adjust if your path differs
        ],
    },
)
