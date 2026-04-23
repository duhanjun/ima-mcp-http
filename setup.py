from setuptools import setup, find_packages

setup(
    name="ima_mcp",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "urllib3"
    ],
    author="IMA MCP Team",
    author_email="",
    description="IMA OpenAPI MCP Service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
