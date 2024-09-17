# JARVIS Development Process

## Using AI Assistance (e.g., Cursor)

1. **Create and Reference Prompt Files**:
   - Store project-specific guidelines in the `prompts/` directory.
   - Always reference relevant prompt files when giving instructions to AI.
   Example: "Implement a new agent following @prompts/coding-standards.md and @prompts/agent-guidelines.md"

2. **Thorough Code Review**:
   - Review every line of AI-generated code carefully.
   - Do not accept changes blindly.
   - Make incremental changes and improvements.

3. **Encourage AI to Ask Questions**:
   - End your prompts with: "Ask any and all questions you might have that makes the instructions clearer"
   - Address AI's questions to provide clearer context and requirements.

4. **Iterative Development**:
   - Break down large tasks into smaller, manageable chunks.
   - Implement features incrementally, reviewing and testing at each step.

5. **Documentation**:
   - Update relevant documentation as you develop.
   - Ensure README, setup instructions, and API docs are kept up-to-date.

6. **Testing**:
   - Write unit tests for all new functionality.
   - Ensure all tests pass before submitting a pull request.

7. **Code Style and Standards**:
   - Adhere to the coding standards defined in @prompts/coding-standards.md
   - Use linters and formatters to maintain consistent code style.

Remember, AI is a tool to assist development, not replace critical thinking and problem-solving skills. Always apply your expertise and judgment in the development process.