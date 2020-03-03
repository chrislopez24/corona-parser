import requests

class WorldOMeterGateway:
    @staticmethod
    def fetch():
        url = "https://www.worldometers.info/coronavirus/#countries"

        try:
            res = requests.get(url, timeout=15)
        except requests.Timeout:
            raise WorldOMeterGatewayError("Timeout received whilst retrieving data from WorldOMeter")
        except requests.RequestException:
            raise WorldOMeterGatewayError("Some Error Ocurred whils fetching data from WorldOMeter({str(requests.RequestException)})")

        if res.status_code != 200:
            raise WorldOMeterGatewayError("Website returned a Non-200 status code")

        return res.text

class WorldOMeterGatewayError(Exception):
    pass 