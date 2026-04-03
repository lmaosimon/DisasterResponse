import unittest

from api.app import create_app


class DisasterResponseApiTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_catalog_lists_supported_disasters_and_locations(self):
        response = self.client.get("/api/v1/catalog")

        self.assertEqual(200, response.status_code)
        payload = response.get_json()
        self.assertIn("earthquake", payload["disasters"])
        self.assertIn("midwest", payload["locations"])

    def test_create_session_returns_first_report(self):
        response = self.client.post(
            "/api/v1/sessions",
            json={
                "disaster": "earthquake",
                "location": "midwest",
                "population": 1000,
            },
        )

        self.assertEqual(201, response.status_code)
        payload = response.get_json()
        self.assertEqual("earthquake", payload["disaster"])
        self.assertEqual("midwest", payload["location"])
        self.assertEqual(0, payload["step"])
        self.assertIsInstance(payload["report"], str)
        self.assertTrue(payload["report"])

    def test_record_action_advances_session(self):
        create_response = self.client.post(
            "/api/v1/sessions",
            json={
                "disaster": "earthquake",
                "location": "midwest",
                "population": 1000,
            },
        )
        session_id = create_response.get_json()["session_id"]

        action_response = self.client.post(
            f"/api/v1/sessions/{session_id}/actions",
            json={"action": "declare_emergency"},
        )

        self.assertEqual(200, action_response.status_code)
        payload = action_response.get_json()
        self.assertEqual(1, payload["step"])
        self.assertEqual(["declare_emergency"], payload["actions_taken"])


if __name__ == "__main__":
    unittest.main()
