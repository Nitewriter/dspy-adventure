import dspy


class SummaryModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.Predict("narrative -> summary")

    def forward(self, narrative: str) -> str:
        pred = self.prog(narrative=narrative)

        summary_text = pred["summary"]

        if "Summary:" in summary_text:
            summary_text = summary_text.split("Summary:")[1].strip()

        return summary_text
