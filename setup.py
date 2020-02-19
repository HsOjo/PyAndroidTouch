#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name="PyAndroidTouch",
    version="0.0.1",
    author="HsOjo",
    author_email="hsojo@qq.com",
    keywords='hsojo python3 android ojopyadb touch',
    description='''Python3 Android Touch Module, Base On "BobbleKeyboard/android_touch". Support Multi-Finger Tap/Swipe/Circle/Expand Action...''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HsOjo/PyAndroidTouch/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
