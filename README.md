# DSPy Adventure

This is a text adventure game built using DSPy. The narrative is generated using a language model.

## Language Models Supported

- Mistral using Ollama local
- GPT-3.5 turbo using OpenAI API

## How to Play

1. Create a virtual environment and install the dependencies

```bash
python3 -m venv venv
source venv/bin/activate

python -m pip install poetry
poetry install
```

2. Run the game

```bash
poetry run python -m adventure
```

## Known Issues

- Tons of bugs (LOL)
- The language model responses do not always follow a consistent structure
  - Malformed player backstories
  - Malformed game narratives
  - Malformed story summaries
  - Malformed encounter text
  - Malformed menu options
  - Malformed encounter resolution
- The narrative context is lost over time
- The player can't explore the game world
- The player can be stuck in a single encounter loop forever
- DSPy can crash sometimes

## Roadmap

- [x] Add narrative generation
- [x] Add player creation
- [x] Add random encounters
- [x] Add language model selection
- [x] Add player created game context
- [x] Add game narrative display (Story so far)
- [x] Add game quit
- [ ] Add player controlled exploration/travel
- [ ] Upgrade encounter system
- [ ] Add player stats
- [ ] Add inventory system
- [ ] Add companion system
- [ ] Add textual UI
- [ ] Add location breadcrumbs
- [ ] Upgrade exploration system
- [ ] Upgrade shop system
- [ ] Add vector database with document store
- [ ] Retrieve game context from database