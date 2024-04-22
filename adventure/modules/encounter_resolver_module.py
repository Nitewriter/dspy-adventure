from enum import StrEnum

import dspy


class EncounterResolution(StrEnum):
    RESOLVED_SUCCESS = "resolved_success"
    RESOLVED_FAILURE = "resolved_failure"
    UNRESOLVED = "unresolved"

    @classmethod
    def types_csv(cls):
        return ", ".join([f"'{e.name}'" for e in cls])


class EncounterResolverModule(dspy.Module):
    def __init__(self):
        super().__init__()
        instruction = f"Given an encounter description, return the outcome of the player action as ({EncounterResolution.types_csv()}) and noting else."
        self.action_outcome_resolver = dspy.Predict(
            dspy.Signature(
                "encounter, player_character -> outcome",
                instruction,
            )
        )

    def forward(self, encounter: str, player_character: str) -> EncounterResolution:
        pred = self.action_outcome_resolver(
            encounter=encounter, player_character=player_character
        )

        outcome_text = pred["outcome"]

        if "Outcome:" in outcome_text:
            outcome_text = outcome_text.split("Outcome:")[1].strip()

        outcome_text = outcome_text.lower()
        # remove special characters
        outcome_text = "".join(e for e in outcome_text if e.isalnum())

        try:
            resolution = EncounterResolution(outcome_text)
        except ValueError:
            # Error on the side of the encounter being in progress
            print(f"[debug]: Unable to resolve outcome '{outcome_text}'")
            resolution = EncounterResolution.UNRESOLVED

        return resolution
