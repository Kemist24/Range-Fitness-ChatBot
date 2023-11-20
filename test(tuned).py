from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio

app = FastAPI()

# Create a dictionary to store user responses
user_responses = {}

# Define a model for the webhook request
class WebhookRequest(BaseModel):
    responseId: str
    queryResult: dict

# Define workout plans (unchanged)
workout_plans = [
    {
        "name": "Beginner Weight Loss Plan",
        "description": "https://drive.google.com/file/d/1Zid0TdwXbEc0NC4UTXL3Jnj8BPnMJrO-/view",
        "gender": "any",
        "experience-level": "beginner",
        "fitness-goal": "cutting",
        "preferred-days": ["4"],
        "equipment-preference": "dumbell",
    },
    {
        "name": "Intermediate Muscle Gain Plan",
        "description": "https://drive.google.com/file/d/1M-_ArEqjOsVCoysWuMU-XdfnhiMKXyeb/view",
        "gender": "any",
        "experience-level": "intermediate",
        "fitness-goal": "bulking",
        "preferred-days": ["5"],
        "equipment-preference": "barbells",
    },
    {
        "name": "Advanced Endurance Plan",
        "description": "https://drive.google.com/file/d/1aLHZ9ThHEunYHNYecC46U-SpQxuajcGv/view",
        "gender": "any",
        "experience-level": "advanced",
        "fitness-goal": "cutting",
        "preferred-days": ["six"],
        "equipment-preference": "dumbell",
    },
    {
        "name": "Women's Strength Training",
        "description": "https://drive.google.com/file/d/1iIPa_n073MJAn8VC0OkfwXUHaLE-TqRn/view",
        "gender": "female",
        "experience-level": "beginner",
        "fitness-goal": "cutting",
        "preferred-days": ["five"],
        "equipment-preference": "dumbbell",
    },
    {
        "name": "Bodyweight Home Workout",
        "description": "https://drive.google.com/file/d/1YRs1WYiJHSAXQYNXTbhtfjuQvhqU2ec8/view",
        "gender": "any",
        "experience-level": "beginner",
        "fitness-goal": "bulking",
        "preferred-days": ["four"],
        "equipment-preference": "barbells",
    },
    # You can add more workout plans as needed
]

# Define a model for the response
class Response(BaseModel):
    fulfillmentText: str

# Webhook endpoint to receive and route requests
@app.post("/")
async def webhook_handler(webhook_request: WebhookRequest, background_tasks: BackgroundTasks):
    query_result = webhook_request.queryResult
    session_id = query_result.get("outputContexts")[0].get("name")
    intent_name = query_result.get("intent").get("displayName")

    suitable_plans = find_workout_plans(gender, experience_level, fitness_goal, preferred_days, equipment_preference)

    # Implement asynchronous background tasks for non-blocking operations
    background_tasks.add_task(process_user_input, query_result)

   
    # Extract user responses from query_result
    user_response = query_result.get("queryText")

    # Store user responses in the user_responses dictionary based on the intent
    if intent_name == "gender to experience-level-intent":
        gender = query_result.get("parameters", {}).get("gender", "Unknown")
    elif intent_name == "experience-level-to-goal intent":
        experience_level = query_result.get("parameters").get("experience-level")
    elif intent_name == "fitness-goal to preferred-days":
        fitness_goal = query_result.get("parameters").get("fitness-goal")
    elif intent_name == "preffered-days to equipment-preference":
        preferred_days = query_result.get("parameters").get("preferred-days")
    elif intent_name == "workout.plan.complete":
        equipment_preference = query_result.get("parameters").get("equipment-preference")

    # Continue the conversation to collect the remaining preferences
    if intent_name == "gender to experience-level-intent":
        return {}
    elif intent_name == "experience-level-to-goal intent":
        return {}
    elif intent_name == "fitness-goal to preferred-days":
        return {}
    elif intent_name == "preffered-days to equipment-preference":
        return {}
    elif intent_name == "workout.plan.complete":
        
            fulfillment_text = "check the following link for your workout plan: https://drive.google.com/file/d/1wjFuShz5pvsW6jbf__eLvuMPM9PZ_7qv/view"
            return Response(fulfillmentText=fulfillment_text)

        # Format and return suitable plans to the user
    if suitable_plans:
        response_message = "Here are some suitable workout plans for you:\n"
        for plan in suitable_plans:
                response_message += f"- {plan['name']} ({plan['duration']})\n"
    else:
         response_message = "Sorry, no workout plans match your preferences."


# Implementing asynchronous background tasks
async def process_user_input(query_result):
    # Extract and process user input asynchronously
    # Store user responses asynchronously
    await asyncio.sleep(1)  # Simulated asynchronous processing
    user_response = query_result.get("queryText")
    # Store user responses in the user_responses dictionary based on the intent
    

# Function to find suitable workout plans based on user preferences (unchanged)
def find_workout_plans(gender, experience_level, fitness_goal, preferred_days, equipment_preference):
    suitable_plans = []

    for plan in workout_plans:
        if (
            (plan["gender"] == "any" or plan["gender"] == gender) and
            plan["experience-level"] == experience_level and
            plan["fitness-goal"] == fitness_goal and
            (preferred_days in plan["preferred-days"]) and
            (equipment_preference in plan["equipment-preference"])
        ):
            suitable_plans.append(plan)

    return suitable_plans

# Start the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
