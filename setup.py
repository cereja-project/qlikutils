import setuptools

REQUIRED_PACKAGES = ['Pillow']

setuptools.setup(
        name="qlikutils",
        version="1.0.1",
        author="Kin Torres",
        author_email="kin.mello@gmail.com",
        description="Toolkit to use with Qlik",
        include_package_data=True,
        packages=setuptools.find_packages(),
        package_data={"assets": ["*.png"]},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=REQUIRED_PACKAGES
)