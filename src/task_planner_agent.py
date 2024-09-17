import os
from typing import List, Dict, Optional
from llama_index import VectorStoreIndex, Document
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.callbacks import CallbackManager
from llama_index.llms import OpenAI
from logger import setup_logger
import spacy
from PIL import Image
import torch
import torchvision
from dotenv import load_dotenv

load_dotenv()

task_planner_logger = setup_logger('task_planner', 'logs/task_planner.log')

class TaskPlannerAgent:
    def __init__(self, knowledge_base: VectorStoreIndex):
        self.knowledge_base = knowledge_base
        self.llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), temperature=0, model="gpt-3.5-turbo")
        self.callback_manager = CallbackManager([])
        self.nlp = spacy.load("en_core_web_sm")
        self.object_detection_model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.object_detection_model.eval()

    def decompose_task(self, query: str) -> List[str]:
        doc = self.nlp(query)
        # This is a simple example. In a real application, you'd use more sophisticated NLP techniques.
        subtasks = []
        for sent in doc.sents:
            subtasks.append(sent.text)
        return subtasks

    def create_query_engine(self) -> SubQuestionQueryEngine:
        """Create a query engine with tools for different types of tasks."""
        tools = [
            QueryEngineTool(
                query_engine=self.knowledge_base.as_query_engine(),
                metadata=ToolMetadata(
                    name="knowledge_base",
                    description="Useful for answering questions about AI, machine learning, and related topics"
                )
            ),
            # Add more tools here for different types of tasks
        ]

        return SubQuestionQueryEngine.from_defaults(
            query_engine_tools=tools,
            llm=self.llm,
            callback_manager=self.callback_manager,
        )

    def execute_task(self, query: str) -> Dict[str, str]:
        """Execute a task by decomposing it and running subtasks."""
        task_planner_logger.info(f"Received task: {query}")
        subtasks = self.decompose_task(query)
        task_planner_logger.info(f"Decomposed into subtasks: {subtasks}")

        query_engine = self.create_query_engine()
        results = {}

        for subtask in subtasks:
            task_planner_logger.info(f"Executing subtask: {subtask}")
            response = query_engine.query(subtask)
            results[subtask] = str(response)
            task_planner_logger.info(f"Subtask result: {results[subtask]}")

        return results

    def synthesize_results(self, results: Dict[str, str]) -> str:
        """Synthesize results from subtasks into a coherent response."""
        synthesis_prompt = "Synthesize the following results into a coherent response:\n"
        for subtask, result in results.items():
            synthesis_prompt += f"{subtask}: {result}\n"

        response = self.llm.complete(synthesis_prompt)
        return response.text

    def process_image(self, image_filename: str) -> str:
        """Process the uploaded image and return a description with detected objects."""
        if not image_filename:
            return ""

        image_path = os.path.join('uploads', image_filename)
        if not os.path.exists(image_path):
            task_planner_logger.error(f"Image file not found: {image_path}")
            return f"Error: Image file '{image_filename}' not found."

        try:
            with Image.open(image_path) as img:
                width, height = img.size

            # Perform object detection
            img_tensor = torchvision.transforms.functional.to_tensor(img)
            with torch.no_grad():
                prediction = self.object_detection_model([img_tensor])[0]

            # Filter detections with confidence > 0.5
            mask = prediction['scores'] > 0.5
            boxes = prediction['boxes'][mask].tolist()
            labels = [self.object_detection_model.COCO_INSTANCE_CATEGORY_NAMES[i] for i in prediction['labels'][mask].tolist()]

            # Create description
            description = f"The uploaded image '{image_filename}' has dimensions {width}x{height}. "
            if labels:
                description += f"Detected objects: {', '.join(labels)}."
            else:
                description += "No objects were detected with high confidence."

            return description
        except Exception as e:
            task_planner_logger.error(f"Error processing image {image_filename}: {str(e)}")
            return f"Error processing image '{image_filename}': {str(e)}"

    def process_query(self, query: str, image_filename: Optional[str] = None) -> str:
        """Process a user query by executing tasks and synthesizing results."""
        image_description = self.process_image(image_filename) if image_filename else ""
        if image_description:
            query = f"{query} (Image context: {image_description})"

        task_results = self.execute_task(query)
        final_response = self.synthesize_results(task_results)
        task_planner_logger.info(f"Final response: {final_response}")
        return final_response