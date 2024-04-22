from enum import StrEnum, auto

import dspy

from adventure.utils import strip_numbered_prefixes


class LocationType(StrEnum):
    CITY_TOWN = auto()
    WILDERNESS = auto()

    def signature(self):
        signatures = {
            LocationType.CITY_TOWN: "Imagine named cities/towns that fit the narrative.",
            LocationType.WILDERNESS: "Imagine named wilderness areas that fit the narrative.",
        }
        return signatures[self]


class LocationModule(dspy.Module):
    def __init__(self, location_type: LocationType):
        super().__init__()

        instructions = f"{location_type.signature()} Return a numbered list of locations and noting else."
        signature = dspy.Signature(
            "narrative -> locations",
            instructions,
        )

        self.location_type = location_type
        self.prog = dspy.Predict(signature)

    def forward(self, narrative: str) -> list[str]:
        pred = self.prog(narrative=narrative)

        locations_text = pred["locations"]

        if "Locations:" in locations_text:
            locations_text = locations_text.split("Locations:")[1].strip()

        raw_locations = locations_text.split("\n")
        if len(raw_locations) == 1:
            raw_locations = locations_text.split(", ")

        locations: list[str] = []
        for location in raw_locations:
            location = strip_numbered_prefixes(location)
            location = location.split(" - ")[0].strip()
            location = location.split(": ")[0].strip()
            locations.append(location)

        return locations
