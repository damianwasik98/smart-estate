# asari-crm-tools

Small API that automates client data entry to [Asari CRM](https://asaricrm.com/).

This tool helps my friend who owns real estate agency. Now it's possible to save data to CRM right after phonecall with client. All using your voice while driving a car.

## Usage
I created iOS shortcut to gather data using voice and send note to API. Then API makes requests to CRM on user behalf with data from iOS shortcut.

## Tests

To run tests you'll need to export groq api key.
You can find it in [Groq Dev Console](https://console.groq.com/keys).
```sh
export GROQ_API_KEY="<your key>"
```

To run all tests just type
```
pytest tests
```

