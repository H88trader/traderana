import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='traderana',
    version='0.1.0',
    author='H88trader',
    author_email='boruotrading@gmail.com',
    description='A Package that tracking trades',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/H88trader/traderana',
    project_urls = {
        "Bug Tracker": "https://github.com/H88trader/traderana/issues"
    },
    license='GNU GENERAL PUBLIC LICENSE v3.0',
    packages=['traderana'],
    install_requires=[
                       'cycler',
                       'et-xmlfile',
                       'fonttools',
                       'kiwisolver',
                       'matplotlib',
                       'numpy',
                       'openpyxl',
                       'packaging',
                       'pandas',
                       'Pillow',
                       'pyparsing',
                       'python-dateutil',
                       'pytz',
                       'six',
                     ]
)