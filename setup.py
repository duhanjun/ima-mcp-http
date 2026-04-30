from setuptools import setup, find_packages

setup(
    name="ima-mcp-http",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "urllib3",
        "fastapi",
        "uvicorn",
        "pydantic"
    ],
    author="Du Hanjun",
    author_email="hanjun.du@outlook.com",
    description="IMA OpenAPI MCP HTTP Service",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'ima-mcp-http=ima_mcp_http.main:main',
        ],
    },
)
