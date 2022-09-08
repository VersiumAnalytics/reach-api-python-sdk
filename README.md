# Versium Reach API Software Development Kit (SDK)
A simplified Python interface for appending data using [Versium Reach APIs](https://api-documentation.versium.com/docs/start-building-with-versium)

## Installation
It's recommended that you first create a virtual Python environment before installing using tools such as virtualenv or 
conda. This is to prevent you from installing the package directly onto your system's base Python installation. Once
you have created and activated your virtual environment, proceed with the steps below.

1) Clone or download the codebase from the [GitHub Page](https://github.com/VersiumAnalytics/reach-api-python-sdk)
2) CD into the newly downloaded or cloned folder
```bash
cd reach-api-python-sdk
```
3) Now install the package with pip
```bash
pip install .
```

## Usage

1) Import ReachClient into your program
```python
from reach import ReachClient
```
2) Pass your [API Key](https://app.versium.com/account/manage-api-keys) to the ReachClient constructor.
```python
client = ReachClient('api-key-012345678')
```
3) Run the `append` method of your `ReachClient` object with the API name, input records, desired outputs (if applicable),
and any extra config parameters you wish to pass.
```python

```