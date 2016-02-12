from setuptools import setup, find_packages

setup(
    name="vk_wall_poster",
    version='0.1.0',
    description='Django module for vk wall poster',
    author='Spi4ka',
    packages=[
        "vk_wall_poster",
    ],
    install_requires=[
        'requests',
    ]
)