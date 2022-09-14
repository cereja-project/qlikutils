import setuptools

REQUIRED_PACKAGES = ['Pillow']

setuptools.setup(
    name="qlikutils",
    version="1.0.9",
    author="Kin Torres",
    author_email="kin.mello@gmail.com",
    description="Toolkit to use with Qlik",
    packages=setuptools.find_namespace_packages(),
    package_data={
        "qlik.assets": ["*"],
        "qlik.assets.images": ["*.png"],
        "qlik.assets.fonts": ["*.ttf"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=REQUIRED_PACKAGES
)
