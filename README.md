# Versium Reach API Software Development Kit (SDK)
A simplified Python interface for appending data using [Versium Reach APIs](https://api-documentation.versium.com/docs/start-building-with-versium)

## Installation
It's recommended that you first create a virtual Python environment before installing using tools such as virtualenv or 
conda. This is to prevent you from installing the package directly onto your system's base Python installation. Once
you have created and activated your virtual environment, proceed with one of the steps below.

## PyPI
```bash
pip install versium-reach-sdk
```
## Install from Source
1) Clone or download the codebase from the [GitHub Page](https://github.com/VersiumAnalytics/reach-api-python-sdk)
2) CD into the newly downloaded or cloned folder
```bash
cd reach-path-python-sdk
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
client = ReachClient('path-key-012345678')
```
3) Run the `append` method of your `ReachClient` object with the API name, input records, desired outputs (if applicable),
and any extra config parameters you wish to pass.
```python
records = [{"first": "John", 
            "last": "Smith",
            "address": "123 Main St.",
            "city": "New York",
            "state": "NY"}]

results = client.append(api_name="contact",
                        input_records=records,
                        outputs=["phone", "email"],
                        config_params={"match_type": "indiv"})
```

## Returned Results
Results are returned as a list of QueryResult objects, which contain the following attributes:

- **body** : 
        The parsed body of the response from the Versium Reach API.


- **success** :
        Indicates whether the request returned with a successful status code.


- **match_found** :
        Indicates whether a match was found for the queried record


- **http_status** :
        The http status code for the response.


- **reason**:
        Explanation of the http status code (e.g. 200 => "OK", 404 => "Not Found", 401 => "Unauthorized", etc.)


- **headers**:
        The headers of the response.


- **body_raw**:
        The body of the response as raw bytes


- **request_error**:
        If the client errored out during a request, this stores the error object


# Things to keep in mind
- The default rate limit for Reach APIs is 20 queries per second
- You must have a provisioned API key for this function to work. If you are unsure where to find your API key, 
look at our [API key documentation](https://api-documentation.versium.com/docs/find-your-api-key)