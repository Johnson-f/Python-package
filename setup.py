import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setuptools.setup(
    name="marketdata-providers",
    version="1.0.0",
    author="Johnson Nifemi",
    author_email="johnsonnifemi@example.com",
    description="A comprehensive Python package for fetching market data from multiple financial data providers with intelligent failover and caching.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsonnifemi/marketdata-providers",
    project_urls={
        "Bug Tracker": "https://github.com/johnsonnifemi/marketdata-providers/issues",
        "Documentation": "https://github.com/johnsonnifemi/marketdata-providers#readme",
        "Source Code": "https://github.com/johnsonnifemi/marketdata-providers",
    },
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    keywords=[
        "financial", "market-data", "stocks", "api", "trading", "finance",
        "alpha-vantage", "finnhub", "polygon", "twelve-data", "fmp", "tiingo",
        "economic-data", "options", "fundamentals", "news", "earnings"
    ],
    entry_points={
        "console_scripts": [
            "marketdata-cli=marketdata_providers.cli:main",
        ],
    },
)
