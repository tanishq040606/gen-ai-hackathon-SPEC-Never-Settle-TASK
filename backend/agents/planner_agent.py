class PlannerAgent:
    def create_plan(self, research_goal: str):
        """
        Breaks a research goal into actionable research steps
        """
        plan = {
            "goal": research_goal,
            "steps": [
                "Search for relevant academic papers",
                "Filter papers by relevance and recency",
                "Read and extract key sections from papers",
                "Generate structured summaries",
                "Enable contextual question answering"
            ],
            "num_papers": 5
        }
        return plan
