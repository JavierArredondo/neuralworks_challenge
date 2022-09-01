import os

import requests
from flask_restx import Namespace, Resource

endpoint = Namespace("ingestion", description="Queries for ingestion status")

AKHQ_URL = os.getenv("AKHQ_URL", "localhost:8080")
GROUP_ID = os.getenv("GROUP_ID", "test")


@endpoint.route("/status")
@endpoint.response(200, "Success")
class StatusEndpoint(Resource):
    @classmethod
    def _get_lag(cls, topic="trips"):
        url = f"http://{AKHQ_URL}/api/docker-kafka-server/topic/{topic}/groups".strip()
        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", url, headers=headers)
        return response.json()

    @classmethod
    def compute_status(cls, group_id, groups):
        for g in groups:
            if g["id"] == group_id:
                offsets = g["offsets"]
                total = 0
                consumed = 0
                for o in offsets:
                    total += o["lastOffset"]
                    consumed += o["offset"]
                return consumed, total
        return 0, 0

    def get(self):
        status = self._get_lag()
        consumed, total = self.compute_status(GROUP_ID, status)
        return {"status": f"{consumed}/{total}", "advance": float(consumed / total)}
