from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
import yaml
from crewai.tools import tool
from dotenv import load_dotenv
from rpt1.call_rpt1 import RPT1Client
import json
import os
    
load_dotenv()
rpt1_client = RPT1Client()

@tool("call_rpt1")
def call_rpt1(payload: dict) -> str:
    """Function to call RPT-1 model via RPT1Client"""
    response = rpt1_client.post_request(json_payload=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@CrewBase
class MurderMystery():
    """MurderMystery crew"""

    agents_config = "config/agents.yaml"
    tasks_config = 'config/tasks.yaml'

    @agent
    def theft_crime_scene_investigator(self) -> Agent:
        return Agent(
            config=self.agents_config['theft_crime_scene_investigator'], 
            verbose=True,
            tools=[call_rpt1]
        )

    @task
    def inspection_task(self) -> Task:
        return Task(
            config=self.tasks_config['inspection_task'] # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by the @agent decorator
            tasks=self.tasks,    # Automatically collected by the @task decorator.
            process=Process.sequential,
            verbose=True,
        )

def main():
    # Load env vars if needed
    load_dotenv()
    

    # Define the JSON payload for prediction
    payload = {
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

    # read file from evidence/stolen_inventory.json
    with open(os.path.join(os.path.dirname(__file__), "data/evidence/stolen_inventory.json"), "r") as f:
        stolen_rows = json.load(f)
    print("Stolen rows loaded for prediction:", stolen_rows)

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
        "rows": stolen_rows,
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

    #response = rpt1_client.post_request(json_payload=json_payload)
    #print("Prediction response status code:", response.status_code)
    #print("Prediction response JSON:", response.json())

    result = MurderMystery().crew().kickoff(inputs={'payload': payload})
    print("\n📘 Result:\n", result)


if __name__ == "__main__":
    main()
