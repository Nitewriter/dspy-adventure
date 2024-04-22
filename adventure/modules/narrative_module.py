import dspy


class NarrativeModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("player_character, backstory -> narrative")

    def forward(self, player_character: str, backstory: str) -> str:
        pred = self.prog(player_character=player_character, backstory=backstory)

        narrative_text = pred["narrative"]

        if "Narrative:" in narrative_text:
            narrative_text = narrative_text.split("Narrative:")[1].strip()

        if "---" in narrative_text:
            narrative_text = narrative_text.split("---")[0].strip()

        return narrative_text
