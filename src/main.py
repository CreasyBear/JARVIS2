import asyncio
from workflows import run_workflow
from logger import main_logger
from report_generator import report_generator

async def main():
    while True:
        query = input("Enter your query (or 'exit' to quit, 'report' for a task report): ")
        if query.lower() == 'exit':
            break
        elif query.lower() == 'report':
            report = report_generator.generate_report()
            print("Task Report:")
            print(f"Total tasks: {report['total_tasks']}")
            print(f"Task types: {dict(report['task_types'])}")
            print(f"Total cost: ${report['total_cost']:.6f}")
            print(f"Average duration: {report['average_duration']:.2f} seconds")
            if report['most_expensive_task']:
                print(f"Most expensive task: {report['most_expensive_task']['query']} (${report['most_expensive_task']['cost']:.6f})")
            if report['longest_task']:
                print(f"Longest task: {report['longest_task']['query']} ({report['longest_task']['duration']:.2f} seconds)")
        else:
            try:
                result = await run_workflow(query)
                if isinstance(result, dict) and 'error' in result:
                    print(f"An error occurred: {result['result']}")
                else:
                    print("Result:", result['result'])
                    print(f"Estimated cost for this query: ${result['estimated_cost']:.6f}")
            except Exception as e:
                main_logger.error(f"An error occurred: {str(e)}")
                print("I apologize, but an unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    asyncio.run(main())