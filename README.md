# 🧠 Gemini Travel Planner — AI Multi-Agent Travel Assistant

A multi-agent AI assistant built with Google’s **Gemini API** and **Chainlit**, designed to plan personalized travel experiences from start to finish.

---

## 🔍 Overview

1. **Destination Agent**  
   Suggests calming, fun, or themed destinations based on your mood or interest (e.g. happy picnic with family → Lucerne, Switzerland).

2. **Booking Agent**  
   Simulates flight and hotel bookings using realistic mock data.

3. **Explore Agent**  
   Recommends top attractions and iconic local foods for your chosen destination.

4. **Triage Agent (Coordinator)**  
   Orchestrates the flow:  
   - Calls the Destination Agent  
   - Passes output to Booking Agent  
   - Finalizes with Explore Agent  
   - Returns a complete, concise travel plan

---

## 🚀 Features

- ✅ Mood-based **destination suggestions**  
- ✅ Simulated **flight + hotel booking** estimates  
- ✅ Curated **attractions & food** recommendations  
- ✅ Built using streamlined architecture in a **single `main.py` file**

---

## 🧩 Tech Stack

- **Chainlit** – Conversational UI framework  
- **Google Gemini API** – Core LLM backend  
- **Python** – Entire logic implemented in `main.py`  
- **dotenv** – For secure API key management

---

## 🎬 Example Interaction

**User**:  
> I’m feeling happy and want to go on a calm picnic with my family.

**Assistant**:  
**🗺️ Suggested Destination:** Lucerne, Switzerland  
**✈️ Booking Simulation**  
• Flight: Emirates — Karachi → Zurich, Aug 10–15 ($780/person)  
• Hotel: Hotel des Balances — Family Suite ($200/night)  
**📍 Explore & Eat**  
• Attractions: Lake Lucerne Boat Ride, Mount Rigi Scenic Train, Chapel Bridge  
• Local Foods: Cheese Fondue, Rösti, Swiss Hot Chocolate  

---

## 📦 Installation

```bash
pip install chainlit python-dotenv google-generativeai

