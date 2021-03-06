from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="GPGame",
    version="2020.0.2",
    author="Nishant Vikramaditya",
    author_email="junk4Nv7@gmail.com",
    description="An abstraction layer on the Kivy GPU accelerated engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nv7-GitHub/GPGame",
    packages=["GPGame"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["Kivy"]
)
