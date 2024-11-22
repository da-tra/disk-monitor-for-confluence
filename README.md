# Disk Monitor for Confluence

Disk Monitor for Confluence - A tool for displaying capacity of mounted storage devices on a Conluence page.

> WARNING: This project is in an early stage of development and should be used with caution.

## Requirements

* Python >= 3.11
* [Confluence](https://www.atlassian.com/de/software/confluence) account + API key
* Confluence page (content gets overwritten)

## Usage

Disk Monitor for Confluence reads a user-created file `configuration.py`.
`configuration.py`  stores credentials for a Confluence page and paths of the storages devices to be monitored

#### Example config:
```python
# Enter the base URL of the Confluence space to be written to
confluence_base_url = "https://a-confluence-space.atlassian.net/"
# Enter the page ID of the page to be written to. It needs to already exist.
confluence_page_id = 111111
# Enter the name (title) of the Confluence page
confluence_page_name = "a-confluence-page"
# Enter the username from which the page is to be updated
confluence_username = "mail@provider.com"
# Enter the api key for the Confluence space 
api_key = "an-api-key"

# List the paths of all drives to be monitored (starting with "/").
drive_paths = [
    "/path1",
    "/path2",
    ]
```