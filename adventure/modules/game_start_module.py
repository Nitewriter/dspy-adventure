import random

import dspy

from adventure.models import GameContextResponse

# Import modules directly to avoid circular imports
from adventure.modules.backstory_module import BackstoryModule
from adventure.modules.location_module import LocationModule, LocationType
from adventure.modules.narrative_module import NarrativeModule
from adventure.modules.summary_module import SummaryModule


class GameStartModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.backstory_generator = BackstoryModule()
        self.narrative_generator = NarrativeModule()
        self.summary_generator = SummaryModule()
        self.city_generator = LocationModule(LocationType.CITY_TOWN)
        self.wilderness_generator = LocationModule(LocationType.WILDERNESS)

    def forward(
        self, player_character: str, game_description: str
    ) -> GameContextResponse:
        backstory = self.backstory_generator(
            player_character=player_character,
            game_description=game_description,
        )
        narrative = self.narrative_generator(
            player_character=player_character, backstory=backstory
        )
        summary = self.summary_generator(
            narrative=narrative,
        )
        cities_towns = self.city_generator(
            narrative=narrative,
        )
        wilds = self.wilderness_generator(
            narrative=narrative,
        )

        current_location = random.choice(cities_towns + wilds)

        return GameContextResponse(
            backstory=backstory,
            narrative=narrative,
            summary=summary,
            encounter_summaries=[],
            player_character=player_character,
            current_location=current_location,
            cities_towns=cities_towns,
            wilds=wilds,
        )
