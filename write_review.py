from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the task description with detailed steps
TASK = """
Go to https://www.sitejabber.com/reviews/only-success.com and write a positive review.
Use these credentials to log in: 
- Email: xfnepyaa68@gmx.com
- Password: FsUPQbcgG

Follow these steps:
1. Navigate to the website
2. Click on "Write a Review" or similar button
3. If asked to log in, use the provided credentials
4. Write a positive 5-star review with a title and detailed content about excellent customer service, product quality, and fast shipping
5. Submit the review
6. After submission, report what happened and if there was a confirmation message
"""

async def main():
    # Initialize the LLM (make sure you have OPENAI_API_KEY in your .env file)
    llm = ChatOpenAI(model="gpt-4o")
    
    # Create the Browser-Use agent
    agent = Agent(
        task=TASK,
        llm=llm,
    )
    
    # Run the agent and get the result
    result = await agent.run()
    
    # Print the result
    print("Agent completed with result:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 