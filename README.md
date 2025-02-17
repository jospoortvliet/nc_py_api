<p align="center">
    <img src="https://raw.githubusercontent.com/cloud-py-api/nc_py_api/main/docs/resources/nc_py_api_logo.png" width="250" alt="NcPyApi logo">
</p>

# Official Nextcloud Python Framework

[![Analysis & Coverage](https://github.com/cloud-py-api/nc_py_api/actions/workflows/analysis-coverage.yml/badge.svg)](https://github.com/cloud-py-api/nc_py_api/actions/workflows/analysis-coverage.yml)
[![Docs](https://github.com/cloud-py-api/nc_py_api/actions/workflows/docs.yml/badge.svg)](https://cloud-py-api.github.io/nc_py_api/)
[![codecov](https://codecov.io/github/cloud-py-api/nc_py_api/branch/main/graph/badge.svg?token=C91PL3FYDQ)](https://codecov.io/github/cloud-py-api/nc_py_api)

![NextcloudVersion](https://img.shields.io/badge/Nextcloud-26%20%7C%2027%20%7C%2028-blue)
![PythonVersion](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![impl](https://img.shields.io/pypi/implementation/nc_py_api)
![pypi](https://img.shields.io/pypi/v/nc_py_api.svg)

Python library that provides a robust and well-documented API that allows developers to interact with and extend Nextcloud's functionality.

### The key features are:
 * **Fast**: High performance, and as low-latency as possible.
 * **Intuitive**: Fast to code, easy to use.
 * **Reliable**: Minimum number of incompatible changes.
 * **Robust**: All code is covered with tests as much as possible.
 * **Easy**: Designed to be easy to use with excellent documentation.

### Capabilities
| **_Capability_** | Nextcloud 26 | Nextcloud 27 | Nextcloud 28 |
|------------------|:------------:|:------------:|:------------:|
| Filesystem*      |      ✅       |      ✅       |      ✅       |
| Shares           |      ✅       |      ✅       |      ✅       |
| Users & Groups   |      ✅       |      ✅       |      ✅       |
| User status      |      ✅       |      ✅       |      ✅       |
| Weather status   |      ✅       |      ✅       |      ✅       |
| Notifications    |      ✅       |      ✅       |      ✅       |
| Nextcloud Talk   |      ❌       |      ❌       |      ❌       |
| Text Provider**  |      ❌       |      ❌       |      ❌       |

&ast;missing `Trash bin` and `File version` support.<br>
&ast;&ast;available only for NextcloudApp

### Differences between the NextCloud and NextCloudApp classes

The **NextCloud** class functions as a standard NextCloud client,
enabling you to make API requests using a username and password.

On the other hand, the **NextCloudApp** class is designed for creating applications for NextCloud.<br>
It uses the [AppEcosystem](https://github.com/cloud-py-api/app_ecosystem_v2) to allow
applications to impersonate users through a separate authentication mechanism.

Both classes offer most of the same APIs,
but NextCloudApp has a broader selection since applications typically require access to more APIs.

Any code written for the NextCloud class can easily be adapted for use with the NextCloudApp class,
as long as it doesn't involve calls that require user password verification.

### Support

You can support us in several ways:

- ⭐️ Star our work (it really motivates)
- ❗️ Create an Issue or feature request (bring to us an excellent idea)
- 💁 Resolve some Issue or create a Pull Request (contribute to this project)
- 🙏 Write an example of its use or correct a typo in the documentation.

## More Information

- [Documentation](https://cloud-py-api.github.io/nc_py_api/)
  - [First steps](https://cloud-py-api.github.io/nc_py_api/FirstSteps.html)
  - [More APIs](https://cloud-py-api.github.io/nc_py_api/MoreAPIs.html)
  - [Writing a simple Nextcloud application](https://cloud-py-api.github.io/nc_py_api/NextcloudApp.html)
  - [Writing a Nextcloud System Application](https://cloud-py-api.github.io/nc_py_api/NextcloudSysApp.html)
- [Examples](https://github.com/cloud-py-api/nc_py_api/tree/main/examples)
- [Contribute](https://github.com/cloud-py-api/nc_py_api/blob/main/.github/CONTRIBUTING.md)
  - [Discussions](https://github.com/cloud-py-api/nc_py_api/discussions)
  - [Issues](https://github.com/cloud-py-api/nc_py_api/issues)
  - [Setting up dev environment](https://cloud-py-api.github.io/nc_py_api/DevSetup.html)
- [Changelog](https://github.com/cloud-py-api/nc_py_api/blob/main/CHANGELOG.md)

### Motivation

_Python's language, elegant and clear,_<br>
_Weaves logic's threads without fear,_<br>
_And in the sky, where clouds take form,_<br>
_Nextcloud emerges, a digital norm._<br>

_Together they stand, a duo bright,_<br>
_Python and Nextcloud, day and night,_<br>
_In a digital dance, they guide and sail,_<br>
_Shaping tomorrow, where new ideas prevail._<br>

#### **Know that we are always here to support and assist you on your journey.**
### P.S: **_Good luck, and we hope you have fun!_**
