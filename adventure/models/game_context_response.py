from pydantic import BaseModel


class GameContextResponse(BaseModel):
    backstory: str
    narrative: str
    summary: str
    encounter_summaries: list[str]

    player_character: str
    current_location: str
    cities_towns: list[str]
    wilds: list[str]
