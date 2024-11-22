# Disk Monitor for Confluence

Disk Monitor for Confluence - A tool for displaying capacity of mounted storage devices on a Conluence page.

> WARNING: This project is in an early stage of development and should be used with caution.

## Requirements

* Python >= 3.11
* [Confluence](https://www.atlassian.com/de/software/confluence) account + API key
* Confluence page (content gets overwritten)

## Usage

Disk Monitor for Confluence reads a user-created file `configuration.py`, which stores credentials for a Confluence page, a Confluence user and their API key, as well as a list of the storages devices to be monitored, identified via their mounted file paths.

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

Disk Monitor for Confluence extracts information about storage device capacity and writes them to the defined Confluence page, including a timestamp.

### Example output
```markdown
| path   | storage                                       | time of snapshot     |
|--------|-----------------------------------------------|----------------------|
| /path1 | used: 47.8 %  free: 214.79 GBtotal: 455.59 GB |  22-11-2024 14:12:56 |
| /path2 | used: 15.6 %  free: 0.84 GBtotal: 1.00 GB     |  22-11-2024 14:12:56 |
```

