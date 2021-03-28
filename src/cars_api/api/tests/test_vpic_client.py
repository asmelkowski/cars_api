from unittest.mock import Mock, patch

import requests
from api.vpic_client import VpicClient
from django.test import TestCase

PATCHING_PATH = "api.vpic_client"


class VpicClientTestCase(TestCase):
    def setUp(self):
        self.instance = VpicClient("https://idonotexsist.com")

    def test___init__(self):
        self.assertEqual(self.instance.base_url, "https://idonotexsist.com")

    @patch(f"{PATCHING_PATH}.logger")
    def test__handle_response(self, mock_logger):
        mock_response = Mock()
        mock_response.status_code = 200
        self.instance._handle_response(mock_response)
        mock_logger.assert_not_called()
        mock_response.json.assert_called_once_with()

        mock_logger.reset_mock()
        mock_response.reset_mock()

        mock_response.status_code = 404
        self.instance._handle_response(mock_response)
        mock_logger.error.assert_called_once_with(
            "Remote server did not response with succesful response\n"
            "It responded with %s status code.".format(404)
        )
        mock_response.json.assert_not_called()
        mock_response.raise_for_status.assert_called_once_with()

        mock_logger.reset_mock()
        mock_response.reset_mock()

        mock_response.status_code = 200
        mock_response.json.side_effect = Exception
        with self.assertRaises(Exception):
            self.instance._handle_response(mock_response)
        mock_logger.error.assert_called_once_with(
            "There was an error decoding the response",
            exc_info=True,
        )
        mock_response.json.assert_called_once_with()

    @patch(f"{PATCHING_PATH}.VpicClient._handle_response")
    def test__call(self, mock__handle_response):
        mock_request_method = Mock()
        mock_request_method.return_value = "test response"
        self.instance._call(
            mock_request_method,
            "/api/v51/test_endpoint",
            {"language": "es", "mobile": True},
            {"test": "data"},
            {"test": "json"},
        )
        mock_request_method.assert_called_once_with(
            "https://idonotexsist.com/api/v51/test_endpoint",
            params={"language": "es", "mobile": True},
            data={"test": "data"},
            json={"test": "json"},
        )
        mock__handle_response.assert_called_once_with("test response")

    @patch(f"{PATCHING_PATH}.VpicClient._call")
    def test_get_models_for_make(self, mock__call):
        self.instance.get_models_for_make("ford")
        mock__call.assert_called_once_with(
            method=requests.get,
            path=f"getmodelsformake/ford",
            query_params={"format": "json"},
        )

    @patch(f"{PATCHING_PATH}.VpicClient.get_models_for_make")
    def test_validate_model_for_make(self, mock_get_models_for_make):
        mock_get_models_for_make.return_value = {
            "Results": [
                {"Model_Name": "Kugga"},
                {"Model_Name": "K"},
                {"Model_Name": "Fiesta"},
                {"Model_Name": "Focus"},
            ]
        }
        result = self.instance.validate_model_for_make("ford", "focus")
        mock_get_models_for_make.assert_called_once_with("ford")
        self.assertTrue(result)

        mock_get_models_for_make.reset_mock()
        mock_get_models_for_make.return_value = {
            "Results": [
                {"Model_Name": "Kugga"},
                {"Model_Name": "K"},
                {"Model_Name": "Fiesta"},
            ]
        }
        result = self.instance.validate_model_for_make("ford", "focus")
        mock_get_models_for_make.assert_called_once_with("ford")
        self.assertFalse(result)
