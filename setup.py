from pathlib import Path
from setuptools import setup, find_packages

PACKAGE_DIR = Path(__file__).parent.absolute()
REQUIREMENTS_TXT = PACKAGE_DIR / "requirements.txt"

assert REQUIREMENTS_TXT.exists(), "Requirements file not found"

packages = find_packages(PACKAGE_DIR)

package_data = {
    package: [
        '*.py',
        '*.txt',
        '*.json',
        '*.npy'
    ]
    for package in packages
}

dependencies = REQUIREMENTS_TXT.read_text().split()

setup(
    name='adscores',
    version='0.0.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='deep-learning anomaly-detection benchmarking',
    packages=packages,
    package_data=package_data,
    install_requires=dependencies,
)
