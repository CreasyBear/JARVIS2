from typing import Dict

class CostEstimator:
    def __init__(self):
        # Define cost per token for different models/services
        self.cost_per_token = {
            "gpt-3.5-turbo": 0.002 / 1000,  # $0.002 per 1K tokens
            "text-embedding-ada-002": 0.0004 / 1000,  # $0.0004 per 1K tokens
            "summarization": 0.001 / 1000,  # Example cost for summarization
            "calculation": 0.0005 / 1000,  # Example cost for calculation
        }

    def estimate_cost(self, service: str, token_count: int) -> float:
        """
        Estimate the cost for using a specific service.

        :param service: The name of the service or model
        :param token_count: The number of tokens processed
        :return: Estimated cost in USD
        """
        if service not in self.cost_per_token:
            raise ValueError(f"Unknown service: {service}")

        return self.cost_per_token[service] * token_count

    def estimate_workflow_cost(self, usage: Dict[str, int]) -> float:
        """
        Estimate the total cost for a workflow.

        :param usage: A dictionary with services as keys and token counts as values
        :return: Total estimated cost in USD
        """
        total_cost = 0.0
        for service, token_count in usage.items():
            total_cost += self.estimate_cost(service, token_count)
        return total_cost

cost_estimator = CostEstimator()