from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os
import poplib
import email
from email.header import decode_header
import time
import re
import sys
import subprocess

# Check required packages
required_packages = ["poplib", "langchain_openai", "browser_use", "python-dotenv"]
missing_packages = []

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f"Missing required packages: {', '.join(missing_packages)}")
    print("Installing missing packages...")
    for package in missing_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except Exception as e:
            print(f"Failed to install {package}: {e}")
            sys.exit(1)
    print("All required packages installed. Restarting script...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

# Load environment variables
load_dotenv()

# Email credentials
EMAIL = "xfnepyaa68@gmx.com"
PASSWORD = "FsUPQbcgG"

# Create the task description with detailed steps
TASK = """
Follow these steps in order:
1. Navigate DIRECTLY to https://www.trustpilot.com/evaluate/only-success.com
2. Fill out the review form with the following information:
   - Rating: 5 stars (click on the rightmost star)
   - Fill out the title field with "Excellent service with high-quality results"
   - Review text: Write a positive review (at least 100 words) about only-success.com. Mention that it's a company that sells followers, likes, etc. in highest quality with the power of AI. Describe how their service exceeded expectations, had fast delivery, and provided excellent customer support.
   - Choose a random review date
   - Click "Continue with email" and enter the email: xfnepyaa68@gmx.com
   - Your name: Use a random name (any realistic name)
   - If there are any additional fields (like location, verification checkbox, etc.), fill them out appropriately
3. Submit the review by clicking the submit button
4. IMPORTANT: After submitting the review, wait for a verification code. DO NOT go to GMX webmail yourself.
   - The system will automatically check for the verification code and display it to you
   - Look for text that says "CONFIRMATION CODE: XXXXX" either in the console output or in a text file called "confirmation_code.txt"
   - If you see this code, enter it in the verification field on Trustpilot
5. Complete all remaining steps until the review is successfully posted
6. Report the entire process and outcome in detail
"""

def get_confirmation_code():
    """
    Fetch confirmation code from GMX email via POP3
    Returns the confirmation code or None if not found
    """
    print("Attempting to fetch confirmation code from email...")
    
    # Connect to GMX POP3 server
    pop_server = "pop.gmx.com"
    pop_port = 995
    
    # Try multiple times to get the email with the confirmation code
    for attempt in range(10):
        try:
            print(f"Attempt {attempt+1} to check email...")
            server = poplib.POP3_SSL(pop_server, pop_port)
            server.user(EMAIL)
            server.pass_(PASSWORD)
            
            # Get email statistics
            stat = server.stat()
            print(f"Total emails: {stat[0]}, Total size: {stat[1]} bytes")
            
            # Get all emails (most recent first)
            num_messages = stat[0]
            if num_messages == 0:
                print("No emails found. Waiting before retrying...")
                server.quit()
                time.sleep(30)  # Wait 30 seconds before checking again
                continue
                
            # Check the most recent 5 emails (or all if less than 5)
            for i in range(min(5, num_messages)):
                msg_num = num_messages - i
                response, lines, octets = server.retr(msg_num)
                
                # Parse the email content
                msg_content = b'\r\n'.join(lines).decode('utf-8', errors='ignore')
                msg = email.message_from_string(msg_content)
                
                # Get email subject
                subject = ""
                if msg["Subject"]:
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8', errors='ignore')
                
                # Check if this is from Trustpilot
                if "trustpilot" in subject.lower() or "verification" in subject.lower() or "confirm" in subject.lower():
                    print(f"Found email with subject: {subject}")
                    
                    # Extract confirmation code from the email
                    confirmation_code = None
                    
                    # Look for the code in the email body
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain" or content_type == "text/html":
                                try:
                                    # Fixed: use get_payload with decode=True and then decode the bytes
                                    payload = part.get_payload(decode=True)
                                    if isinstance(payload, bytes):
                                        body = payload.decode('utf-8', errors='ignore')
                                    else:
                                        body = str(payload)
                                    # Look for confirmation code patterns
                                    # Pattern 1: digits only (4-8 digits)
                                    digit_codes = re.findall(r'\b\d{4,8}\b', body)
                                    if digit_codes:
                                        confirmation_code = digit_codes[0]
                                        print(f"Found confirmation code: {confirmation_code}")
                                        server.quit()
                                        return confirmation_code
                                    
                                    # Pattern 2: alphanumeric code (common format)
                                    alpha_codes = re.findall(r'\b[A-Z0-9]{4,8}\b', body)
                                    if alpha_codes:
                                        confirmation_code = alpha_codes[0]
                                        print(f"Found confirmation code: {confirmation_code}")
                                        server.quit()
                                        return confirmation_code
                                except:
                                    continue
                    else:
                        try:
                            # Fixed: use get_payload with decode=True and then decode the bytes
                            payload = msg.get_payload(decode=True)
                            if isinstance(payload, bytes):
                                body = payload.decode('utf-8', errors='ignore')
                            else:
                                body = str(payload)
                            # Same code extraction logic as above
                            digit_codes = re.findall(r'\b\d{4,8}\b', body)
                            if digit_codes:
                                confirmation_code = digit_codes[0]
                                print(f"Found confirmation code: {confirmation_code}")
                                server.quit()
                                return confirmation_code
                            
                            alpha_codes = re.findall(r'\b[A-Z0-9]{4,8}\b', body)
                            if alpha_codes:
                                confirmation_code = alpha_codes[0]
                                print(f"Found confirmation code: {confirmation_code}")
                                server.quit()
                                return confirmation_code
                        except:
                            continue
            
            server.quit()
            print("Confirmation code not found in current emails. Waiting before retrying...")
            time.sleep(30)  # Wait 30 seconds before checking again
            
        except Exception as e:
            print(f"Error checking email: {str(e)}")
            time.sleep(30)  # Wait 30 seconds before retrying
    
    print("Failed to find confirmation code after multiple attempts")
    return None

async def main():
    # Initialize the LLM (make sure you have OPENAI_API_KEY in your .env file)
    llm = ChatOpenAI(model="gpt-4o")
    
    # Create a shared file for communication with the agent
    code_file_path = "confirmation_code.txt"
    with open(code_file_path, "w") as f:
        f.write("Waiting for confirmation code...\n")
        f.write("This file will be updated automatically when the code is retrieved.")
    
    # Create the Browser-Use agent
    agent = Agent(
        task=TASK,
        llm=llm,
        use_vision=True
    )
    
    # Start the agent process
    agent_task = asyncio.create_task(agent.run())
    
    # Wait a bit for the agent to submit the review
    await asyncio.sleep(120)  # Wait 2 minutes for the agent to potentially submit the review
    
    # Start checking for the confirmation code
    code_check_task = asyncio.create_task(check_for_code(code_file_path))
    
    # Wait for either the agent to finish or the code check to complete
    done, pending = await asyncio.wait(
        [agent_task, code_check_task], 
        return_when=asyncio.FIRST_COMPLETED,
        timeout=900  # 15 minute overall timeout
    )
    
    # Cancel any pending tasks
    for task in pending:
        task.cancel()
    
    # Get the result from the agent task if it completed
    if agent_task in done:
        result = agent_task.result()
    else:
        result = "Agent task did not complete in time"
    
    # Print the result
    print("Agent completed with result:")
    print(result)

async def check_for_code(code_file_path):
    """Periodically check for confirmation code and update the file when found"""
    for _ in range(20):  # Try for about 10 minutes (20 * 30s)
        # Get the confirmation code
        confirmation_code = get_confirmation_code()
        
        if confirmation_code:
            print(f"\n\n=== CONFIRMATION CODE: {confirmation_code} ===\n\n")
            
            # Update the file with the code
            with open(code_file_path, "w") as f:
                f.write(f"CONFIRMATION CODE: {confirmation_code}\n")
                f.write("Please use this code to complete your verification on Trustpilot.\n")
                f.write("Enter this code in the verification field and continue with the process.")
            
            print(f"Updated confirmation code file at {code_file_path}")
            print(f"Please enter the confirmation code: {confirmation_code}")
            
            # Wait a bit to make sure the agent has time to use the code
            await asyncio.sleep(300)  # Wait 5 minutes for agent to use the code
            return confirmation_code
        
        print("Confirmation code not found yet. Waiting...")
        await asyncio.sleep(30)  # Wait 30 seconds before checking again
    
    print("Unable to find a confirmation code after multiple attempts")
    with open(code_file_path, "w") as f:
        f.write("NO CONFIRMATION CODE FOUND\n")
        f.write("Please check if the review was submitted correctly or try again.")
    
    return None

if __name__ == "__main__":
    asyncio.run(main()) 