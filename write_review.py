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
These are the credentials for the email address:
- Email: xfnepyaa68@gmx.com
- Password: FsUPQbcgG

Follow these steps:
1. Navigate to the website
2. Click on "Write a Review" or similar button
3. Use the email address provided and use a random name.
4. Write a positive 5-star review with a title and detailed content about excellent customer service, product quality, and fast shipping
5. Submit the review
6. After submission, log into the email address in the webmail at https://www.gmx.com by:
   - Going to https://www.gmx.com
   - Clicking on "Log in"
   - Entering the email: xfnepyaa68@gmx.com
   - Entering the password: FsUPQbcgG
   - Looking for the confirmation email from Sitejabber
   - Opening the email and clicking on the confirmation link
7. Report the entire process and outcome
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