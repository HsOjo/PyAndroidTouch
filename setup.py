#!/usr/bin/env python
import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()


def gen_data_files(*dirs):
    results = []
    for src_dir in dirs:
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file[0] == '.':
                    files.remove(file)
            results.append((root, list(map(lambda f: root + "/" + f, files))))
    return results


setuptools.setup(
    name="PyAndroidTouch",
    version="0.0.2",
    author="HsOjo",
    author_email="hsojo@qq.com",
    keywords='hsojo python3 android ojopyadb touch',
    description='''Python3 Android Touch Module, Base On "BobbleKeyboard/android_touch". Support Multi-Finger Tap/Swipe/Circle/Expand Action...''',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HsOjo/PyAndroidTouch/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
    data_files=gen_data_files('pyandroidtouch/libs'),
)
