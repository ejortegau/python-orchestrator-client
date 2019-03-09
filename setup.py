import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-orchestrator-client",
    version="0.1a1",
    author="Eduardo Javier Ortega Urrego",
    author_email="ejortegau at mainstream google email service",
    description="A python client for Orchestrator",
    long_description="A python client for Orchestrator",
    url="https://github.com/ejortegau/python-orchestrator-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3.0",
        "Operating System :: OS Independent",
    ],
)
