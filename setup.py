import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crypto-analysis-cli-datacryptoanalytics", # Replace with your own username
    version="0.0.1",
    author="Felipe Soares",
    author_email="contato@datacryptoanalytics.com",
    description="Analyze Cryptocurrencies on the Binance Exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/datacrypto-analytics/crypto-analysis-cli",
    packages=setuptools.find_packages(),
    classifiers=[
		"Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
		"Framework :: Matplotlib",
    ],
    python_requires='>=3.6',
)
