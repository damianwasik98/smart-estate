# smart-estate

Save data to [Asari CRM](https://asaricrm.com/) using your voice.

This small API helps my friend who owns real estate agency. Now it's possible to save data to CRM right after phonecall with client. All using your voice while driving a car.
I used LLM to parse natural language voice memo to structured format.

## Usage

I created iOS shortcut as an user interface for sending text note to API.
User shares phone number to the shortcut and then summarize phonecall using voice. THen automatically API is called from shortcut.

## Development

To run this project you need to create `.env` file with correct configs and run

```sh
docker-compose -f docker-compose.yaml -f docker-compose.dev.yaml watch
```

It will sync files between local repo and container.

## Tests

To run all tests just type

```
pytest tests
```

### Integration tests

To run integration tests you'll need to export groq api key.
You can find it in [Groq Dev Console](https://console.groq.com/keys).

```sh
export GROQ_API_KEY="<your key>"
```
