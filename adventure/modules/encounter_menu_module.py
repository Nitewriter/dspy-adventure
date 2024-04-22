import dspy

from adventure.utils import strip_numbered_prefixes


class EncounterMenuModule(dspy.Module):
    def __init__(self):
        super().__init__()
        # Seems to provide menu choices that could have lead to the encounter
        instruct_v1 = "Given an encounter description, return a numbered list of menu choices and noting else."
        # Seems to forget who the player is, providing menu choices from a different character's perspective
        instruct_v2 = "Imagine menu choices that would advance the story. Return a numbered list of these choices and nothing else."
        # Seems to provide the type of menu choices that we want
        instruct_v3 = "Imagine menu choices from the players perspective that would advance the story. Return a numbered list of these choices and nothing else."
        self.prog = dspy.Predict(
            dspy.Signature(
                "encounter -> menu",
                instruct_v3,
            )
        )

    def forward(
        self,
        encounter: str,
    ) -> list[str]:
        pred = self.prog(
            encounter=encounter,
        )

        menu_text = pred["menu"]

        if "Menu:" in menu_text:
            menu_text = menu_text.split("Menu:")[1].strip()

        # remove any leading mentions of choices by the model
        if ":\n" in menu_text:
            menu_text = menu_text.split(":\n")[1].strip()

        options = []
        for option in menu_text.split("\n"):
            option = option.strip()
            option = strip_numbered_prefixes(option)
            option = option.strip()

            if len(option) > 0:
                options.append(option)

        if len(options) == 0:
            return ["Explore the area", "Look around", "Check inventory", "Rest"]

        # Only take the first 5 options
        options = options[:5]

        return options
