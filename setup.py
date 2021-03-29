import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rebornos-welcome",
    version="0.0.1",
    author="Shivanand Pattanshetti",
    author_email="shivanandvp@rebornos.org",
    description="RebornOS Welcome is the application that would display on the RebornOS ISO and on first use of RebornOS after installation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rebornos-team/applications/rebornos-welcome",
    download_url="https://gitlab.com/rebornos-team/applications/rebornos-welcome",
    project_urls={
        'Documentation': 'https://rebornos-team.gitlab.io/applications/rebornos-welcome/',
        'Source': 'https://gitlab.com/rebornos-team/applications/rebornos-welcome',
        'Tracker': 'https://gitlab.com/rebornos-team/applications/rebornos-welcome/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        # "Typing :: Typed",
        "Topic :: System :: Operating System",
    ],
    install_requires = [
        'fenix-library-running >= 0.0.7',
        'fenix-library-configuration >= 0.0.3',
        'pygobject',
        'numpy',
    ],
    packages=setuptools.find_packages(where="."),
    python_requires='>=3.6'
)