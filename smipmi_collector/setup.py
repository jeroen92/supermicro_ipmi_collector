from setuptools import setup, find_packages

setup(
    name="smipmic",
    version="0.0.1",
    packages=find_packages(),
    description="Supermicro IPMI Collector",
    author="Jeroen Schutrup",
    author_email="jeroenschutrup@hotmail.nl",
    scripts=['smipmi_collector'],
    zip_safe=True,
    install_requires=[
        'prometheus_client',
    ],
)
