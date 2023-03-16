# pfizer_project_repo
Repository for pfizer project 


# Whois Change Checker

This is a Python script that checks for changes in WHOIS data for a list of domains, and sends an email with the changes if any are found.

## Usage

1. Clone this repository to your local machine.
2. Install the required packages by running `pip install -r requirements.txt` in your terminal.
3. In`constants.py`file , replace the placeholders with your own values.
4. You'll need to obtain an API key from https://whois.whoisxmlapi.com/.
5. Edit the `DOMAINS` list in `constants.py` to include the domains you want to check.
6. Run the `check_changes()` method in the `WhoisChangeChecker` class to start the script.
7. The script will run continuously, checking for changes every 24 hours . If any changes are found, the script will create a JSON file with the changed results, and send an email with the JSON file attached.

## Classes

### `WhoisAPI`

This class handles querying the WHOIS API for a single domain, and parsing the response data. It has two methods:

- `query_api()`: Sends a GET request to the WHOIS API with the specified domain, and returns the response data as a JSON object.
- `parse_data(whois_data)`: Parses the response data from the WHOIS API, and returns a dictionary with the domain's WHOIS data.

### `WhoisChangeChecker`

This class handles checking for changes in WHOIS data for a list of domains, and sending an email if any changes are found. It has one method:

- `check_changes()`: Runs the script continuously, checking for changes every 30 seconds. If any changes are found, the script will create a JSON file with the changed results, and send an email with the JSON file attached.

## License

This script is licensed under the MIT License. See the `LICENSE` file for details.