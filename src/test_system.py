import asyncio
from workflows import run_workflow, JARVISWorkflow
from logger import main_logger
import json

async def setup():
    # Initialize any necessary resources
    main_logger.info("Setting up test environment")
    # You might want to initialize a test database or mock certain services here

async def teardown():
    # Clean up resources
    main_logger.info("Tearing down test environment")
    # Clean up any test data or connections here

async def test_system():
    test_queries = [
        ("information", "What is the capital of France?"),
        ("calculation", "Calculate the average of 10, 15, and 20"),
        ("summarization", "Summarize the following text: The quick brown fox jumps over the lazy dog. This sentence is often used for testing typography and keyboard layouts."),
        ("action", "How do I bake a chocolate cake?"),
        ("web_scraping", "Scrape and summarize the content from https://en.wikipedia.org/wiki/Artificial_intelligence"),
        ("error", "This is an intentional error to test error handling"),
        ("complex", "Research the impact of climate change on polar bear populations, summarize the findings, and suggest three actionable steps to mitigate the effects."),
    ]

    results = {"passed": 0, "failed": 0}

    for category, query in test_queries:
        main_logger.info(f"Testing {category} query: {query}")
        try:
            # Test planning step
            workflow = JARVISWorkflow()
            plan = await workflow.plan_task({"query": query})
            assert isinstance(json.loads(plan.result), dict), f"Invalid plan structure for {category} query"
            main_logger.info(f"Planning step passed for {category} query")

            # Test full workflow
            result = await run_workflow(query)
            if isinstance(result, dict) and 'error' in result:
                assert category == "error", f"Unexpected error in {category} query: {result['result']}"
                main_logger.info(f"Error handling test passed: {result['result']}")
            else:
                assert 'result' in result, f"Missing 'result' in response for {category} query"
                assert 'estimated_cost' in result, f"Missing 'estimated_cost' in response for {category} query"
                assert result['estimated_cost'] > 0, f"Estimated cost should be greater than 0 for {category} query"

                if category == "information":
                    assert "Paris" in result['result'], "The capital of France (Paris) should be in the result"
                elif category == "calculation":
                    assert "15" in result['result'], "The average of 10, 15, and 20 (15) should be in the result"
                elif category == "summarization":
                    assert "fox" in result['result'] and "dog" in result['result'], "The summary should contain key words from the original text"
                elif category == "action":
                    assert "ingredients" in result['result'].lower() or "steps" in result['result'].lower(), "The cake recipe should mention ingredients or steps"
                elif category == "web_scraping":
                    assert "artificial intelligence" in result['result'].lower(), "The AI Wikipedia summary should mention 'artificial intelligence'"
                elif category == "complex":
                    assert "climate change" in result['result'].lower() and "polar bear" in result['result'].lower() and "steps" in result['result'].lower(), "The complex query result should mention climate change, polar bears, and actionable steps"

                main_logger.info(f"{category} test passed successfully")
                main_logger.info(f"Estimated cost: ${result['estimated_cost']:.6f}")

            results["passed"] += 1
        except Exception as e:
            if category == "error":
                main_logger.info("Error handling test passed successfully")
                results["passed"] += 1
            else:
                main_logger.error(f"Error processing {category} query '{query}': {str(e)}")
                results["failed"] += 1

    main_logger.info(f"Test summary: {results['passed']} passed, {results['failed']} failed")
    assert results["failed"] == 0, f"{results['failed']} tests failed"

if __name__ == "__main__":
    asyncio.run(setup())
    try:
        asyncio.run(test_system())
    finally:
        asyncio.run(teardown())
