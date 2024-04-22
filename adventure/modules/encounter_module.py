import dspy


class EncounterModule(dspy.Module):
    def __init__(self):
        super().__init__()
        # seems to provide an encounter that takes actions on the behalf of the player beyond the actions that the player took
        instruct_v1 = "Imagine an encounter that fits the context and location for the player to resolve."
        # seems to provide a lead-in encounter that the player can resolve, however, it has a tendency to produce no encounter when the player has resolved it with an action
        instruct_v2 = "Imagine the start of an encounter that fits the context and location for the player to resolve."
        instruct_v3 = "Imagine the next part of an encounter that fits the context and location for the player to resolve."
        self.prog = dspy.Predict(
            dspy.Signature(
                "context, location, player_character -> encounter",
                f"{instruct_v3} Return the encounter description and noting else.",
            )
        )

    def forward(self, context: str, location: str, player_character: str) -> str:
        pred = self.prog(
            context=context, location=location, player_character=player_character
        )

        encounter_text = pred["encounter"]

        if "Encounter:" in encounter_text:
            encounter_text = encounter_text.split("Encounter:")[-1].strip()

        if encounter_text.startswith("Context:"):
            print(f"[error] prediction contains 'Context:'")

        return encounter_text
