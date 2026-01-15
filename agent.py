import asyncio
import os
import logging
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from costAnalyser import get_cost_and_usage
from dotenv import load_dotenv

#Load Environment Variables
load_dotenv()


# Suppress excessive logging
logging.getLogger("google_adk").setLevel(logging.WARNING)

async def main():
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return

    # Database URL for local SQLite with async driver
    db_url = "sqlite+aiosqlite:///agent_sessions.db"

    print("Initializing Agentic Cloud Cost Optimizer...")
    
    # Initialize Session Service (Context Manager handles cleanup)
    async with DatabaseSessionService(db_url=db_url) as session_service:
        
        # Configure Model
        # using a widely available model
        model = Gemini(model="gemini-2.5-flash")
        
        # Initialize Agent with Tools
        agent = Agent(
            name="cost_optimizer",
            model=model,
            tools=[get_cost_and_usage]
        )
        
        # Initialize Runner
        # Initialize Runner
        runner = Runner(
            agent=agent,
            session_service=session_service,
            app_name="cost_app"
        )

        user_id = "user_001"
        session_id = "session_001"
        
        # Check if session exists, create if not
        if not await session_service.get_session(app_name="cost_app", user_id=user_id, session_id=session_id):
            print(f"Creating new session: {session_id}")
            await session_service.create_session(app_name="cost_app", user_id=user_id, session_id=session_id)
        
        print("\nAgent Ready! (Session: Persistent)")
        print("Type 'exit' or 'quit' to stop.")
        
        while True:
            try:
                user_input = input("\nYou: ")
            except EOFError:
                break
                
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if not user_input.strip():
                continue
                
            # Create the message content
            message = types.Content(role="user", parts=[types.Part(text=user_input)])
            
            print("Agent: ", end="", flush=True)
            
            # Run the agent asynchronously
            try:
                async for event in runner.run_async(
                    user_id=user_id, 
                    session_id=session_id, 
                    new_message=message
                ):
                    # Filter and print content events
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                print(part.text, end="", flush=True)
            except Exception as e:
                print(f"\nError during execution: {e}")
                
            print() # Ensure newline after response

if __name__ == "__main__":
    asyncio.run(main())