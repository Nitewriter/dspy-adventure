import random

import dspy
from dotenv import load_dotenv

from adventure.models import GameContextResponse
from adventure.modules import (
    EncounterMenuModule,
    EncounterModule,
    EncounterResolution,
    EncounterResolverModule,
    GameStartModule,
    PointOfInterestModule,
    SummaryModule,
)
from adventure.utils import print_divider

game_start_generator = GameStartModule()
points_of_interest_generator = PointOfInterestModule()

encounter_generator = EncounterModule()
encounter_menu_generator = EncounterMenuModule()
encounter_outcome_resolver = EncounterResolverModule()


summary_generator = SummaryModule()

load_dotenv()

# Consider Textual for a more user-friendly interface
# https://medium.com/short-bits/textual-text-based-uis-in-python-8234f090889a


SUPPORTED_MODELS = ["gpt-3", "mistral", "llama3"]


def load_language_model(model_name: str) -> dspy.LM:
    max_tokens = 2000
    temperature = 0.7
    if model_name == "gpt-3":
        return dspy.OpenAI(
            model="gpt-3.5-turbo",
            max_tokens=max_tokens,
            temperature=temperature,
            # system_prompt=system_prompt,
        )
    elif model_name == "mistral" or model_name == "llama3":
        return dspy.OllamaLocal(
            model=model_name,
            model_type="text",
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=0.5,
            timeout_s=500,
        )
    else:
        raise ValueError(f"Invalid model name: {model_name}")


def get_user_choice(encounter: str) -> str:
    options = encounter_menu_generator(
        encounter=encounter,
    )

    options_dict: dict[int, str] = {}
    print("-" * 80)
    for i, option in enumerate(options, start=1):
        options_dict[i] = option
        print(f"| {i}: {option}")

    print("| 9: Story so far")
    print("| 0: Exit")
    print("-" * 80)

    choice = None
    while choice not in options_dict:
        raw_input = input("Enter the number of your choice: ")
        try:
            choice = int(raw_input)
        except ValueError:
            print("Invalid choice. Try again.")
            continue

        if choice == 0:
            return "exit"
        elif choice == 9:
            return "story"

        if choice not in options_dict:
            print("Invalid choice. Try again.")

    return options_dict[choice]


def get_the_story_so_far(game_context: GameContextResponse) -> str:
    if len(game_context.encounter_summaries) == 0:
        return game_context.narrative

    story_components = []

    for encounter_summary in game_context.encounter_summaries:
        story_components.append(encounter_summary)

    summary_pred = summary_generator(narrative="\n".join(story_components))
    return summary_pred.summary


def try_main():
    # clear the screen
    print("\033[H\033[J")

    model_name = input(f"Select a model ({', '.join(SUPPORTED_MODELS)}): ")
    if model_name == "llama3":
        print_divider("WARNING")
        print("Using llama3 is experimental and generations may be malformed.")
        print_divider()

    try:
        lm = load_language_model(model_name)
    except ValueError as e:
        print(e)
        return

    dspy.configure(lm=lm)

    try:
        main()
    except ValueError as e:
        print(e)
        print("-" * 80)
        lm.inspect_history(n=3)
    except KeyboardInterrupt:
        print("Goodbye!")


def main():
    should_exit = False

    game_description = input("Describe the adventure (1-3 sentences): ")
    player_name = input("Enter your name: ")

    print_divider("Building the adventure")
    print(f" - Backstory for {player_name}")
    print(f" - Narrative for {game_description}")
    print(f" - Summary for the adventure")
    print(f" - Locations for the adventure")
    print("This may take a few moments...")
    print_divider()

    game_context = game_start_generator(
        player_character=player_name, game_description=game_description
    )

    print_divider(f"Welcome, {game_context.player_character}!")
    print(f"[Backstory] {game_context.backstory}\n")
    print(f"[Narrative Summary] {game_context.summary}\n")
    print(f"Your adventure begins at {game_context.current_location}...")
    print_divider()

    last_encounter = encounter_generator(
        context=game_context.summary,
        location=game_context.current_location,
        player_character=game_context.player_character,
    )
    last_outcome = EncounterResolution.UNRESOLVED

    print(f"<{game_context.current_location}> {last_encounter}\n")

    encounter_log = [last_encounter]

    # For each failed encounter, accumulate a bonus to the next roll
    encounter_bonus = 0

    while not should_exit:
        # TODO: - Provide the player with travel options if the encounter is resolved
        choice = get_user_choice(encounter=last_encounter)

        player_choice = f"{game_context.player_character} chooses to: {choice}"
        d20_roll = min(random.randint(1, 20) + encounter_bonus, 20)
        player_rolls = f"{game_context.player_character} rolls a {d20_roll} out of 20 odds of success."

        print("\n")

        if choice == "exit":
            print("Goodbye!")
            should_exit = True
            continue

        elif choice == "story":
            story = get_the_story_so_far(game_context)
            print(f"[STORY] {story}\n")
            continue

        else:
            encounter_so_far = "\n\n".join(encounter_log)
            context = f"{encounter_so_far}\n\n{player_choice}\n\n{player_rolls}"
            last_encounter = encounter_generator(
                context=context,
                location=game_context.current_location,
                player_character=game_context.player_character,
            )

            encounter_log.append(last_encounter)
            encounter_details = f"{player_choice}\n\n{last_encounter}"
            last_outcome = encounter_outcome_resolver(
                encounter=encounter_details,
                player_character=game_context.player_character,
            )

            if last_outcome != EncounterResolution.UNRESOLVED:
                flattened_log = "\n".join(encounter_log)
                summary = summary_generator(narrative=flattened_log)
                game_context.encounter_summaries.append(summary)
                encounter_log = [summary]

            if last_outcome == EncounterResolution.RESOLVED_SUCCESS:
                encounter_bonus = 0

            if last_outcome == EncounterResolution.RESOLVED_FAILURE:
                encounter_bonus += 1

        print(f"<{game_context.current_location}> {last_encounter}\n")


if __name__ == "__main__":
    try_main()
