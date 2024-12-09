# Disk Monitor for Confluence

Disk Monitor for Confluence - A tool for displaying capacity of mounted storage devices on a Conluence page and warning via mail if a capacity limit is reached.

> WARNING: This project is in an early stage of development and should be used with caution.

## Requirements

* Python >= 3.12
* smtplib
* [Requests](https://pypi.org/project/requests/)
* [Confluence](https://www.atlassian.com/de/software/confluence) account + API key
* Confluence page (content gets overwritten)

## Usage

Disk Monitor for Confluence reads a user-created file `configuration.py`, which stores: 
* credentials for a Confluence page
* a Confluence user and their API key
* a list of the storages devices to be monitored (identified via their file paths when mounted)
* credentials for a Gmail address that sends notification mails:
  * email address
  * 2-Step Verification code (turn on 2FA [here](https://support.google.com/accounts/answer/185839?hl=en&co=GENIE.Platform%3DDesktop) and get the code [here](https://myaccount.google.com/apppasswords))

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

# List the paths of all drives to be monitored (starting with "/")
drive_paths = [
    "/path1",
    "/path2",
    ]

# Store the credentials for the email address that sends a notification
# when a drive has reached a certain capacity (90%, for instance)
email_sender = "email@gmail.com"
email_2fa = "aaaabbbbccccdddd" # remove all spaces

# Store the receiving email address
email_recipient = "another.email@gmail.com"

# Define the threshold capacity at which a warning is issued in percent (0-100)
capacity_limit: int = 90
```

Disk Monitor for Confluence extracts information about storage device capacity and writes them to the defined Confluence page, including a timestamp.

If any of the drives exceeds a defined capacity, a notification email is sent.

### Example output

<table>
  <tbody>
    <tr>
      <th>
        <p>
          <strong>path</strong>
        </p>
      </th>
      <th>
        <p>
          <strong>storage</strong>
        </p>
      </th>
      <th>
       <p>
         <strong>time of snapshot</strong>
       </p>
      </th>
    </tr>
    <tr>
      <td>
       <p>
         /path1
       </p>
      </td>
      <td>
       <p>
        <strong>used: 25.0 % </strong> <br/>
         free: 100.00 GB<br/>
         total: 400.00 GB<br/>
       </p>
      </td>
      <td>
       <p>
         22-11-2024 14:12:56
        </p>
      </td>
    </tr>
    <tr>
      <td>
       <p>
          /path2
        </p>
      </td>
      <td>
       <p>
          <strong>used: 91.0 % </strong> <br/>
          free: 0.09 GB<br/>
          total: 1.00 GB<br/>
        </p>
      </td>
      <td>
        <p>
          22-11-2024 14:12:56
        </p>
      </td>
    </tr>
  </tbody>
 </table>

### Example email content
>Dear user,
>
>this is an automated notification email, please do not respond to it.
>
>The following drives have exceeded 90 % of storage use:
>
>/path2: 91.00 %


## Program logic
1. Establish a session via the HTTP library Requests
2. Read data about storage capacity from the mounted drives specified in `configuration.py`
3. Create HTML code to display the information
4. GET the version number of the eixisting Confluence page Requests
5. PUT the HTML table on the Confluence page