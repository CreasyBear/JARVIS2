import unittest
from unittest.mock import Mock, patch
from src.task_planner_agent import TaskPlannerAgent

class TestTaskPlannerAgent(unittest.TestCase):
    def setUp(self):
        self.mock_index = Mock()
        self.agent = TaskPlannerAgent(self.mock_index)

    def test_decompose_task(self):
        result = self.agent.decompose_task("Explain machine learning")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    @patch('src.task_planner_agent.SubQuestionQueryEngine')
    def test_execute_task(self, mock_query_engine):
        mock_query_engine.return_value.query.return_value = "Mock response"
        result = self.agent.execute_task("What is AI?")
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

# Add more tests as needed

if __name__ == '__main__':
    unittest.main()