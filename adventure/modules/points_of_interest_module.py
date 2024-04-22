import dspy

from adventure.utils import strip_numbered_prefixes


class PointOfInterestModule(dspy.Module):
    def __init__(self):
        super().__init__()

        signature = dspy.Signature(
            "narrative, primary_location -> locations",
            "Imagine named points of interest that fit the narrative and are related to the primary location. Return a numbered list of locations and noting else.",
        )

        self.prog = dspy.Predict(signature)

    def forward(self, narrative: str, primary_location: str) -> list[str]:
        pred = self.prog(narrative=narrative, primary_location=primary_location)

        locations_text = pred["locations"]

        if "Locations:" in locations_text:
            locations_text = locations_text.split("Locations:")[1].strip()

        locations: list[str] = []
        for location in locations_text.split("\n"):
            location = strip_numbered_prefixes(location)
            location = location.split(" - ")[0].strip()
            location = location.split(": ")[0].strip()
            locations.append(location)

        return locations
