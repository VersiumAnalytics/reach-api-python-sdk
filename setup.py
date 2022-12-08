from distutils.command.clean import clean as Clean
import os
import shutil
from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))


class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"

    def run(self):
        Clean.run(self)
        # Remove c files if we are not within a sdist package
        cwd = os.path.abspath(os.path.dirname(__file__))
        remove_c_files = not os.path.exists(os.path.join(cwd, 'PKG-INFO'))
        if remove_c_files:
            print('Will remove generated .c files')
        if os.path.exists('build'):
            shutil.rmtree('build')
        for dirpath, dirnames, filenames in os.walk('reach'):
            for filename in filenames:
                if any(filename.endswith(suffix) for suffix in
                       (".so", ".pyd", ".dll", ".pyc")):
                    os.unlink(os.path.join(dirpath, filename))
                    continue
                extension = os.path.splitext(filename)[1]
                if remove_c_files and extension in ['.c']:
                    pyx_file = str.replace(filename, extension, '.pyx')
                    if os.path.exists(os.path.join(dirpath, pyx_file)):
                        os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))


def setup_package():
    # Get the long description from the README file
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

    with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        required_packages = f.read().splitlines()

    cmdclass = {'clean': CleanCommand}

    setup(
            name='versium-reach-sdk',
            version='1.0.0',
            description='Python SDK for querying Versium Reach APIs',
            long_description=long_description,
            url='https://github.com/VersiumAnalytics/reach-api-python-sdk',
            author='Versium Analytics, Inc.',
            author_email='opensource@versium.com',
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: BSD License",
                "Operating System :: OS Independent",
            ],
            python_requires='~=3.7',
            zip_safe=False,
            packages=find_packages(),
            package_data={'': ['*.json', '*.j2', '*/*.json', '*/*.j2']},
            install_requires=required_packages,
            cmdclass=cmdclass
    )


if __name__ == "__main__":
    setup_package()
