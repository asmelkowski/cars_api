import logging
from urllib.parse import urljoin

import requests

logger = logging.getLogger("api.vpic_client")


class VpicClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def _handle_response(self, response):
        if response.status_code == 200:
            try:
                return response.json()
            except Exception as exc:
                logger.error(
                    "There was an error decoding the response",
                    exc_info=True,
                )
                raise exc
        else:
            logger.error(
                "Remote server did not response with succesful response\n"
                "It responded with %s status code.".format(response.status_code),
            )
            response.raise_for_status()

    def _call(self, method, path, query_params=None, data=None, json=None):
        response = method(
            urljoin(self.base_url, path), params=query_params, data=data, json=json
        )
        return self._handle_response(response)

    def get_models_for_make(self, make):
        return self._call(
            method=requests.get,
            path=f"getmodelsformake/{make}",
            query_params={"format": "json"},
        )

    def validate_model_for_make(self, make, model):
        cars_data = self.get_models_for_make(make)
        for car in cars_data["Results"]:
            if model_name := car.get("Model_Name"):
                if model_name.lower() == model.lower():
                    return True
        return False
