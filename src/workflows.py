from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.core.workflow import Workflow, StartEvent, StopEvent, step
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding
from llama_index.node_parser import SimpleNodeParser
from llama_index.agent import OpenAIAgent
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.core.workflow.base import WorkflowRunner
from llama_index.deploy import deploy
import asyncio
import os
from logger import workflow_logger
from monitoring import run_monitor
from cost_estimator import cost_estimator
from web_scraping_service import web_scraping_service
from report_generator import report_generator
import time
import json
from planner_agent import planner_agent

# Set up LlamaIndex components
llm = OpenAI(temperature=0, model="gpt-3.5-turbo")
embed_model = OpenAIEmbedding()
node_parser = SimpleNodeParser.from_defaults()
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model, node_parser=node_parser)

class JARVISWorkflow(Workflow):
    def __init__(self):
        super().__init__()
        self.knowledge_base = self._create_knowledge_base()
        self.query_engine = self.knowledge_base.as_query_engine()
        self.openai_agent = self._create_openai_agent()
        self.usage = {}  # To track token usage

    def _create_knowledge_base(self):
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        documents = SimpleDirectoryReader(data_dir).load_data()
        return VectorStoreIndex.from_documents(documents, service_context=service_context)

    def _create_openai_agent(self):
        query_engine_tool = QueryEngineTool(
            query_engine=self.query_engine,
            metadata=ToolMetadata(
                name="knowledge_base",
                description="Useful for answering questions about the knowledge base"
            )
        )
        return OpenAIAgent.from_tools([query_engine_tool], llm=llm)

    @step()
    async def plan_task(self, ev: StartEvent) -> StopEvent:
        query = ev.get("query")
        try:
            plan = await planner_agent.decompose_task(query)
            self.usage["gpt-3.5-turbo"] = self.usage.get("gpt-3.5-turbo", 0) + len(query.split()) + len(plan.split())
            return StopEvent(result=plan, original_query=query)
        except Exception as e:
            workflow_logger.error(f"Error in plan_task: {str(e)}")
            return StopEvent(result=str(e), error=True)

    @step()
    async def execute_plan(self, ev: StartEvent) -> StopEvent:
        plan = json.loads(ev.get("result"))
        original_query = ev.get("original_query")
        results = []

        try:
            for subtask in plan["subtasks"]:
                # Check prerequisites
                for prereq in subtask["prerequisites"]:
                    prereq_result = await self.execute_subtask(prereq, "information")
                    results.append({"task": prereq, "result": prereq_result})

                # Execute subtask
                subtask_result = await self.execute_subtask(subtask["description"], subtask["agent_type"])
                results.append({"task": subtask["description"], "result": subtask_result})

                # Evaluate result
                evaluation = await self.evaluate_subtask(subtask_result, subtask["evaluation"])
                results.append({"task": f"Evaluate: {subtask['description']}", "result": evaluation})

            # Integrate results
            final_result = await self.integrate_results(results, original_query)
            return StopEvent(result=final_result)
        except Exception as e:
            workflow_logger.error(f"Error in execute_plan: {str(e)}")
            return StopEvent(result=str(e), error=True)

    async def execute_subtask(self, task, agent_type):
        try:
            if agent_type == "information":
                result = await information_service_deployed.arun({"query": task})
            elif agent_type == "calculation":
                result = await calculation_service_deployed.arun({"query": task})
            elif agent_type == "summarization":
                result = await summarization_service_deployed.arun({"query": task})
            elif agent_type == "action":
                result = await action_service_deployed.arun({"query": task})
            elif agent_type == "web_scraping":
                result = await web_scraping_service_deployed.arun({"query": task})
            else:
                raise ValueError(f"Unknown agent type: {agent_type}")

            self.usage[agent_type] = self.usage.get(agent_type, 0) + len(task.split()) + len(result.split())
            return result
        except Exception as e:
            workflow_logger.error(f"Error in execute_subtask: {str(e)}")
            raise

    async def evaluate_subtask(self, result, evaluation_criteria):
        prompt = f"Evaluate the following result based on these criteria: {evaluation_criteria}\n\nResult: {result}"
        try:
            evaluation = await self.openai_agent.aquery(prompt)
            self.usage["gpt-3.5-turbo"] = self.usage.get("gpt-3.5-turbo", 0) + len(prompt.split()) + len(evaluation.response.split())
            return evaluation.response
        except Exception as e:
            workflow_logger.error(f"Error in evaluate_subtask: {str(e)}")
            raise

    async def integrate_results(self, results, original_query):
        results_str = "\n".join([f"{r['task']}: {r['result']}" for r in results])
        prompt = f"Given the following subtask results, provide a comprehensive answer to the original query: {original_query}\n\nSubtask results:\n{results_str}"
        try:
            final_result = await self.openai_agent.aquery(prompt)
            self.usage["gpt-3.5-turbo"] = self.usage.get("gpt-3.5-turbo", 0) + len(prompt.split()) + len(final_result.response.split())
            return final_result.response
        except Exception as e:
            workflow_logger.error(f"Error in integrate_results: {str(e)}")
            raise

    @step()
    async def evaluate_response(self, ev: StartEvent) -> StopEvent:
        response = ev.get("result")
        query = ev.get("query")
        evaluation_prompt = f"""
        Evaluate the following response to the query '{query}' for:
        1. Relevance (0-10)
        2. Accuracy (0-10)
        3. Potential for hallucination (0-10, where 0 is no risk and 10 is high risk)
        4. Confidence score (0-100)

        Provide your evaluation in the format:
        Relevance: X
        Accuracy: X
        Hallucination Risk: X
        Confidence: X

        Then provide a brief explanation for your scores.

        Response: {response}
        """
        try:
            evaluation = await self.openai_agent.aquery(evaluation_prompt)
            self.usage["gpt-3.5-turbo"] = self.usage.get("gpt-3.5-turbo", 0) + len(evaluation_prompt.split()) + len(evaluation.response.split())
            return StopEvent(result=evaluation.response)
        except Exception as e:
            workflow_logger.error(f"Error in evaluate_response: {str(e)}")
            return StopEvent(result=str(e), error=True)

    @step()
    async def handle_error(self, ev: StartEvent) -> StopEvent:
        error_msg = ev.get("result")
        workflow_logger.error(f"Handling error: {error_msg}")
        return StopEvent(result=f"An error occurred: {error_msg}")

    @step()
    async def estimate_cost(self, ev: StartEvent) -> StopEvent:
        total_cost = cost_estimator.estimate_workflow_cost(self.usage)
        workflow_logger.info(f"Estimated cost for this workflow: ${total_cost:.6f}")
        return StopEvent(result=ev.get("result"), estimated_cost=total_cost)

    @step()
    async def generate_report(self, ev: StartEvent) -> StopEvent:
        report = report_generator.generate_report()
        workflow_logger.info(f"Generated report: {report}")
        return StopEvent(result=report)

def get_workflow():
    workflow = JARVISWorkflow()

    runner = WorkflowRunner(workflow)
    runner.add_step(workflow.plan_task)
    runner.add_step(workflow.execute_plan)
    runner.add_step(workflow.evaluate_response, condition=lambda ev: not ev.get("error", False))
    runner.add_step(workflow.handle_error, condition=lambda ev: ev.get("error", False))
    runner.add_step(workflow.estimate_cost)
    runner.add_step(workflow.generate_report)

    return runner

# Deploy the main workflow
deployed_workflow = deploy(
    get_workflow(),
    "jarvis_main_workflow",
    description="JARVIS main workflow for task processing",
)

# Deploy individual agent services
information_service_deployed = deploy(
    information_service.execute,
    "information_service",
    description="Service for handling information retrieval tasks",
)

calculation_service_deployed = deploy(
    calculation_service.execute,
    "calculation_service",
    description="Service for handling calculation tasks",
)

summarization_service_deployed = deploy(
    summarization_service.execute,
    "summarization_service",
    description="Service for handling summarization tasks",
)

action_service_deployed = deploy(
    action_service.execute,
    "action_service",
    description="Service for handling action tasks",
)

web_scraping_service_deployed = deploy(
    web_scraping_service.execute,
    "web_scraping_service",
    description="Service for handling web scraping tasks",
)

# Start the monitoring system
asyncio.create_task(run_monitor([information_service_deployed, calculation_service_deployed, summarization_service_deployed, action_service_deployed, web_scraping_service_deployed]))

# Example usage
async def run_workflow(query):
    result = await deployed_workflow.arun({"query": query})
    return result

# This can be called from your main.py or wherever you want to use the workflow
# result = asyncio.run(run_workflow("What is the capital of France?"))
# print(result)