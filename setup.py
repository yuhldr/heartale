"""打包: python setup.py sdist bdist_wheel
"""
import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='heartale',
                 version='0.0.1',
                 author="yuhldr",
                 author_email="yuhldr@qq.com",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 py_modules=["heartale"],
                 install_requires=[
                     "edge_tts >= 6.1.13",
                     "azure-cognitiveservices-speech >= 1.41.1"
                 ],
                 scripts=[
                     "data/scripts/heartale_count",
                     "data/scripts/heartale"
                 ],
                 include_package_data=True,
                 packages=setuptools.find_packages(),
                 description="听书")
