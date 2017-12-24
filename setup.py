from setuptools import setup

PACKAGE = 'pytest-testrail'
VERSION = '0.0.1a'

requirements = [
    'pytest',
    'requests'
]


def main():
    setup(
        name=PACKAGE,
        version=VERSION,
        description="TestRail pytest integration",
        packages=['pytest_testrail'],
        entry_points={
            'pytest11': ['pytest_testrail = pytest_testrail.plugin']
        },
        classifiers=[
            "Framework :: Pytest",
        ],
        install_requires=requirements
    )


if __name__ == '__main__':
    main()
