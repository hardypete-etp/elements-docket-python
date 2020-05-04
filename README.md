# elements-docket-python
# eltech API connection library in python

A python package for connection to and the retrieval, and analysis of production data from Elements Technology Platforms.  A valid subscription to at least the Elements docket production tracking service is required to make any use of this package.

## Installation

### Python Package Library

The most up-to-date production version of this package can be installed from the python package library

`pip install eltech`


### Github

Development versions can be obtained from the [package's github repo](https://github.com/hardypete-etp/elements-docket-python).  This library can be built by moving into the root folder and executing a build command.

`python setup.py sdist bdist_wheel`

This creates build and dist folders in the root directory, the dist folder contains the distributions files in both wheel and tarred formats.  Note:  the wheel file is included as it makes installation in conda environment simpler.  Install can then be run.

`pip install dist/elements-*.*.*-py3-none-any.whl`

Insert correct three component version number for your wheel file.


## Basic Operation

To test the operation of the package, and connection to the Elements servers, this code can be executed.  Ensure that you replace *your_api_key* with a valid api key from the settings page of the elements dashboard.

```
import eltech as el

# Get a Connection object
conn = el.Connection()

# Set the api key
conn.setapikey(your_api_key)

# Make a simple data call
conn.getsnapshot()
```


## Task List

- [ ] Some task
- [ ] Some other task
- [ ] A million possible things that we will never find the time to do
