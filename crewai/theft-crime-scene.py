from crewai import Agent, Crew, Task
from crewai.tools import tool
from dotenv import load_dotenv
from litellm import completion
from rpt1.call_rpt1 import RPT1Client
import os


def main():
    # Load env vars if needed
    load_dotenv()
    rpt1_client = RPT1Client()

    # Define the JSON payload for prediction
    json_payload = {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "COSTCENTER",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "classification",
                },
                {
                    "name": "PRICE",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "regression",
                },
            ]
        },
        "index_column": "ID",
        "rows": [
            {
                "PRODUCT": "Couch",
                "PRICE": "'[PREDICT]'",
                "ORDERDATE": "28-11-2025",
                "ID": "35",
                "COSTCENTER": "'[PREDICT]'",
            },
            {
                "PRODUCT": "Office Chair",
                "PRICE": 150.8,
                "ORDERDATE": "02-11-2025",
                "ID": "44",
                "COSTCENTER": "Office Furniture",
            },
            {
                "PRODUCT": "Server Rack",
                "PRICE": 210.0,
                "ORDERDATE": "01-11-2025",
                "ID": "108",
                "COSTCENTER": "Data Infrastructure",
            },
            {
                "PRODUCT": "Server Rack",
                "PRICE": "'[PREDICT]'",
                "ORDERDATE": "01-11-2025",
                "ID": "104",
                "COSTCENTER": "'[PREDICT]'",
            },
        ],
        "data_schema": {
            "PRODUCT": {"dtype": "string"},
            "PRICE": {"dtype": "numeric"},
            "ORDERDATE": {"dtype": "date"},
            "ID": {"dtype": "string"},
            "COSTCENTER": {"dtype": "string"},
        },
    }

    payload_theft = {
        "prediction_config": {
            "target_columns": [
                {
                    "name": "value",
                    "prediction_placeholder": "'[PREDICT]'",
                    "task_type": "regression",
                }
            ]
        },
        "index_column": "id",
        "rows": [
            {
                "id": 1,
                "type": "necklace",
                "name": "Diamond Solitaire Necklace",
                "value": 15000,
                "description": "18k white gold chain, 2ct diamond, classic design",
                "material": '["diamond", "white gold"]',
                "artist": "n/a",
            },
            {
                "id": 2,
                "type": "necklace",
                "name": "Sapphire Pendant Necklace",
                "value": "'[PREDICT]'",  # 8500 is missing value to be predicted
                "description": "Platinum chain, 1.5ct blue sapphire",
                "material": '["sapphire", "platinum"]',
                "artist": "Tiffany & Co.",
            },
            {
                "id": 3,
                "type": "necklace",
                "name": "Pearl Strand Necklace",
                "value": "[PREDICT]",
                "description": "Freshwater pearls, 14k gold clasp, elegant vintage style",
                "material": '["pearl", "gold"]',
                "artist": "n/a",
            },
            {
                "id": 4,
                "type": "necklace",
                "name": "Emerald Choker",
                "value": 12000,
                "description": "18k gold, 3ct Colombian emeralds",
                "material": '["emerald", "gold"]',
                "artist": "Cartier",
            },
            {
                "id": 5,
                "type": "necklace",
                "name": "Ruby Heart Necklace",
                "value": 6800,
                "description": "18k rose gold, 2ct ruby, heart-shaped pendant",
                "material": '["ruby", "rose gold"]',
                "artist": "n/a",
            },
            {
                "id": 6,
                "type": "watch",
                "name": "Rolex Submariner",
                "value": 13000,
                "description": "Stainless steel, automatic movement, black dial",
                "material": '["stainless steel"]',
                "artist": "Rolex",
            },
            {
                "id": 7,
                "type": "watch",
                "name": "Omega Speedmaster",
                "value": 7500,
                "description": "Stainless steel, chronograph, moonwatch edition",
                "material": '["stainless steel"]',
                "artist": "Omega",
            },
            {
                "id": 8,
                "type": "watch",
                "name": "Patek Philippe Calatrava",
                "value": 22000,
                "description": "18k gold, leather strap, classic dress watch",
                "material": '["gold", "leather"]',
                "artist": "Patek Philippe",
            },
            {
                "id": 9,
                "type": "watch",
                "name": "Audemars Piguet Royal Oak",
                "value": 18000,
                "description": "Stainless steel, blue dial, iconic design",
                "material": '["stainless steel"]',
                "artist": "Audemars Piguet",
            },
            {
                "id": 10,
                "type": "watch",
                "name": "Cartier Tank Solo",
                "value": 5200,
                "description": "Stainless steel, quartz movement, rectangular case",
                "material": '["stainless steel"]',
                "artist": "Cartier",
            },
            {
                "id": 11,
                "type": "earrings",
                "name": "Diamond Stud Earrings",
                "value": 4500,
                "description": "1ct total, 18k white gold, classic studs",
                "material": '["diamond", "white gold"]',
                "artist": "n/a",
            },
            {
                "id": 12,
                "type": "earrings",
                "name": "Sapphire Drop Earrings",
                "value": 3200,
                "description": "14k gold, 2ct blue sapphires",
                "material": '["sapphire", "gold"]',
                "artist": "Bulgari",
            },
            {
                "id": 13,
                "type": "earrings",
                "name": "Pearl Hoop Earrings",
                "value": 1100,
                "description": "Freshwater pearls, sterling silver hoops",
                "material": '["pearl", "silver"]',
                "artist": "n/a",
            },
            {
                "id": 14,
                "type": "earrings",
                "name": "Emerald Cluster Earrings",
                "value": 5800,
                "description": "18k gold, 2ct emeralds, vintage style",
                "material": '["emerald", "gold"]',
                "artist": "n/a",
            },
            {
                "id": 15,
                "type": "earrings",
                "name": "Ruby Teardrop Earrings",
                "value": 2900,
                "description": "14k rose gold, 1.5ct rubies",
                "material": '["ruby", "rose gold"]',
                "artist": "n/a",
            },
            {
                "id": 16,
                "type": "bracelet",
                "name": "Gold Tennis Bracelet",
                "value": 6000,
                "description": "18k gold, 2ct diamonds, classic style",
                "material": '["gold", "diamond"]',
                "artist": "n/a",
            },
            {
                "id": 17,
                "type": "bracelet",
                "name": "Sapphire Bangle",
                "value": 3800,
                "description": "Platinum, 1.2ct sapphires",
                "material": '["sapphire", "platinum"]',
                "artist": "Van Cleef & Arpels",
            },
            {
                "id": 18,
                "type": "bracelet",
                "name": "Pearl Charm Bracelet",
                "value": 1500,
                "description": "Freshwater pearls, 14k gold charms",
                "material": '["pearl", "gold"]',
                "artist": "n/a",
            },
            {
                "id": 19,
                "type": "bracelet",
                "name": "Emerald Cuff Bracelet",
                "value": 7200,
                "description": "18k gold, 2.5ct emeralds, bold design",
                "material": '["emerald", "gold"]',
                "artist": "n/a",
            },
            {
                "id": 20,
                "type": "bracelet",
                "name": "Ruby Link Bracelet",
                "value": 4400,
                "description": "14k gold, 1.8ct rubies",
                "material": '["ruby", "gold"]',
                "artist": "n/a",
            },
            {
                "id": 21,
                "type": "painting",
                "name": "Sunset Over Lake",
                "value": "'[PREDICT]'",  # 25000 is missing value to be predicted
                "description": "Oil on canvas, impressionist landscape",
                "material": '["oil", "canvas"]',
                "artist": "J. Turner",
            },
            {
                "id": 22,
                "type": "painting",
                "name": "Abstract Blue",
                "value": 18000,
                "description": "Acrylic, modern abstract",
                "material": '["acrylic", "canvas"]',
                "artist": "M. Rothko",
            },
            {
                "id": 23,
                "type": "painting",
                "name": "Portrait of Lady",
                "value": 30000,
                "description": "Oil, 19th-century realism",
                "material": '["oil", "canvas"]',
                "artist": "L. Cassatt",
            },
            {
                "id": 24,
                "type": "painting",
                "name": "Cityscape",
                "value": 12000,
                "description": "Watercolor, urban scene",
                "material": '["watercolor", "paper"]',
                "artist": "P. Klee",
            },
            {
                "id": 25,
                "type": "painting",
                "name": "Still Life with Fruit",
                "value": 9500,
                "description": "Oil, post-impressionist",
                "material": '["oil", "canvas"]',
                "artist": "C. Cézanne",
            },
            {
                "id": 26,
                "type": "art_piece",
                "name": "Bronze Sculpture 'The Dancer'",
                "value": 14000,
                "description": "Modernist bronze sculpture",
                "material": '["bronze"]',
                "artist": "H. Moore",
            },
            {
                "id": 27,
                "type": "art_piece",
                "name": "Porcelain Vase",
                "value": 6500,
                "description": "Ming Dynasty, hand-painted blue and white",
                "material": '["porcelain"]',
                "artist": "n/a",
            },
            {
                "id": 28,
                "type": "art_piece",
                "name": "Crystal Chandelier",
                "value": 8200,
                "description": "Baccarat, 24k gold accents, antique",
                "material": '["crystal", "gold"]',
                "artist": "Baccarat",
            },
            {
                "id": 29,
                "type": "art_piece",
                "name": "Marble Bust 'Apollo'",
                "value": 11000,
                "description": "Italian marble, neoclassical style",
                "material": '["marble"]',
                "artist": "n/a",
            },
            {
                "id": 30,
                "type": "art_piece",
                "name": "Silver Goblet Set",
                "value": 4800,
                "description": "19th-century, hand-engraved, 6 pieces",
                "material": '["silver"]',
                "artist": "n/a",
            },
        ],
        "data_schema": {
            "id": {"dtype": "string"},
            "type": {"dtype": "string"},
            "name": {"dtype": "string"},
            "value": {"dtype": "numeric"},
            "description": {"dtype": "string"},
            "material": {"dtype": "string"},
            "artist": {"dtype": "string"},
        },
    }

    response = rpt1_client.post_request(json_payload=payload_theft)
    print("Prediction response status code:", response.status_code)
    print("Prediction response JSON:", response.json())


    @tool("call_rpt1")
    def call_rpt1(payload_theft: dict) -> str:
        """Function to call RPT-1 model via RPT1Client"""
        response = rpt1_client.post_request(json_payload=payload_theft)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"


    theft_crime_scene_investigator = Agent(
        role="Theft Crime Scene Investigator",
        goal="Predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool.",
        backstory="An expert theft crime investigator specialiced on predicting the value of stolen luxury goods.",
        llm="sap/gpt-4o",
        tools=[call_rpt1],
        # multimodal=True,  # This enables multimodal capabilities
    )

    # Create a task for image analysis
    inspection_task = Task(
        description=f"Analyze the theft crime scene and predict the missing values of stolen items using the RPT-1 model via the call_rpt1 tool. Use this payload: {payload_theft} as input.",
        expected_output="JSON with predicted values for the stolen items.",
        agent=theft_crime_scene_investigator,
    )

    # Create and run the crew
    crew = Crew(
        agents=[theft_crime_scene_investigator], tasks=[inspection_task], verbose=True
    )

    result = crew.kickoff()
    print("\n📘 Result:\n", result)


if __name__ == "__main__":
    main()
