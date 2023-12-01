# import inspect
# from azure.messaging.webpubsubservice import WebPubSubServiceClient
# from azure.core.credentials import AzureKeyCredential
# from constants.azure import ENDPOINT, HUB_NAME, ACCESS_KEY


# class AzureConnector:
#     def __init__(self):
#         self._client = WebPubSubServiceClient(
#             hub=HUB_NAME,
#             endpoint=ENDPOINT,
#             credential=AzureKeyCredential(ACCESS_KEY)
#         )

#     def send_message(self, message):
#         self._client.send_to_all(message)

#     def get_client_access_token(self):
#         return self._client.get_client_access_token()

#     def inspect_client(self):
#         properties = {}
#         methods = []

#         # Inspect properties
#         for attr in dir(self._client):
#             if not attr.startswith('_') and not callable(getattr(self._client, attr)):
#                 properties[attr] = getattr(self._client, attr)

#         # Inspect methods
#         for m in inspect.getmembers(self._client, predicate=inspect.ismethod):
#             if not m[0].startswith('_'):
#                 methods.append(m[0])

#         return {
#             'properties': properties,
#             'methods': methods
#         }
