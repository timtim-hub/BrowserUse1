from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the task description with detailed steps
TASK = """
IMPORTANT: Go DIRECTLY to https://www.sitejabber.com/reviews/only-success.com (do not visit any other site first) and write a positive review.

These are the credentials for the email address:
- Email: xfnepyaa68@gmx.com
- Password: FsUPQbcgG

Follow these steps in order:
1. Navigate DIRECTLY to https://www.sitejabber.com/reviews/only-success.com
2. Accept any cookie consent prompts or popups that appear
3. Click on "Write a Review" or similar button
4. Fill out the review form with the following information:
   - Rating: 5 stars (click on the rightmost star)
   - Title: "Excellent service with high-quality results"
   - Review text: Write a positive review (at least 100 words) about only-success.com. Mention that it's a company that sells followers, likes, etc. in highest quality with the power of AI. Describe how their service exceeded expectations, had fast delivery, and provided excellent customer support.
   - Your name: Use a random name (e.g., "Alex Johnson" or any other realistic name)
   - Email: xfnepyaa68@gmx.com
   - If there are any additional fields (like location, verification checkbox, etc.), fill them out appropriately
5. Submit the review by clicking the submit button
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