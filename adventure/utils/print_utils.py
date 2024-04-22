DIVIDER_LENGTH = 80


def print_divider(label: str | None = None):
    if label is None:
        print("-" * DIVIDER_LENGTH)
    else:
        padded_label = f"- {label} "
        print(f"\n{padded_label}" + "-" * (DIVIDER_LENGTH - len(padded_label)))
