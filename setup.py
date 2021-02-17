from setuptools import setup

setup(
    name='sdfgen',
    vesrion=1.0,
    description='Signed distance fields generation on GPUs',
    author='but0n',
    packages=['sdfgen'],
    entry_points={
        'console_scripts': [
            'sdfgen = sdfgen:main',
        ],
    },
    install_requires=[],
    include_package_data=True,
    zip_safe=False,
)