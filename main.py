import os
import chainlit as cl
from typing import cast
from dotenv import load_dotenv
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel

load_dotenv()

external_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(
          model=model,
          model_provider=external_client,
          tracing_disabled=True
     )

destination_agent = Agent(
    name="destination_agent",
    instructions="""
You are a travel destination expert.

Given a user's mood or interest (e.g., happy, romantic, Islamic, adventurous), suggest 1–2 cities or countries ideal for travel. Pick calm, beautiful, family-friendly picnic spots if requested.

Only respond with real travel destinations that match the user's mood. Do not ask questions.
""".strip(),
    handoff_description="Suggests travel destinations based on mood or interests.",
    model=model
)

booking_agent = Agent(
    name="booking_agent",
    instructions="""
You are a travel booking assistant.

Given a destination and approximate dates, generate mock booking info:
- Flight (airline, route, price)
- Hotel (name, room type, cost)

Example:
Destination: Lucerne, Switzerland  
Dates: August 10–15  
• Flight: Emirates — Karachi to Zurich, $780  
• Hotel: Hotel des Balances, $200/night, Family Suite

Do not say "I need more info" — just assume plausible values.
""".strip(),

    handoff_description="Handles booking of flights and hotels.",
    model=model
)

explore_agent = Agent(
    name="explore_agent",
    instructions="""
You are a local travel guide.

Given a destination (city or country), return:
- 2–3 must-see attractions
- 2–3 famous local foods

Be concise and name real locations and dishes from that destination.
""".strip(),
    handoff_description="Recommends top attractions and food in a destination.",
    model=model
)

triage_agent = Agent(
    name="triage_agent",
    instructions="""
You are a travel experience coordinator.

Your job is to plan a complete travel experience by using other agents as tools. Follow this structure step-by-step:

1. First, use the `get_destination_suggestion` tool to suggest a specific **city or country** based on the user's mood or interest.
2. Then use the `simulate_booking` tool with that destination to generate a **mock flight and hotel itinerary**.
3. Finally, use the `get_explore_recommendations` tool to suggest **attractions and local food** in the same destination.

Always combine the results from all tools into a single response. Use clear formatting (e.g., bullet points or headings). Do not answer anything outside of travel planning.

and you don't have to answer by your own, just use given tools.

the output must look like this :
**🗺️ Suggested Destination:** city or country name to visit

**✈️ Booking Simulation**
- **Flight**: airline name — from destination → to destination, date with month (price/person)
- **Hotel**: Hotel name — room type (price/night)

**📍 Places to Explore**
- place to explore 1
- place to explore 2
- place to explore 3

**🍽️ Local Foods**
- food to try 1
- food to try 2
- food to try 3
""".strip(),
    tools=[
        destination_agent.as_tool(
            tool_name="get_destination_suggestion",
            tool_description="Suggests a destination to travel based on user’s mood or interests"
        ),
        booking_agent.as_tool(
            tool_name="simulate_booking",
            tool_description="Simulates travel booking by providing mock flight and hotel options"
        ),
        explore_agent.as_tool(
            tool_name="get_explore_recommendations",
            tool_description="Provides top tourist attractions and famous foods in a destination"
        )
    ],
    model=model
)


@cl.on_message
async def on_message(message: cl.Message):
    result = await Runner.run(triage_agent, message.content)
    await cl.Message(content=result.final_output).send()