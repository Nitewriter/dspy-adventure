import dspy


class BackstoryModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.Predict("player_character, game_description -> backstory")

    def forward(self, player_character: str, game_description: str) -> str:
        pred = self.prog(
            player_character=player_character, game_description=game_description
        )

        backstory_text = pred["backstory"]
        # if contains 'Backstory:' split on that and take the second part
        if "Backstory:" in backstory_text:
            backstory_text = backstory_text.split("Backstory:")[1].strip()
            # Remove any separators returned by the model

        if "---" in backstory_text:
            backstory_text = backstory_text.split("---")[0].strip()

        return backstory_text
