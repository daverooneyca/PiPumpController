import json
import requests
import logging
import traceback

class SlackHandler(logging.Handler):

   hook_url = ""

   def __init__(self, slack_hook_url=""):
      super().__init__()
      self.hook_url = slack_hook_url

   def emit(self, record):
      result = -1

      log_entry = self.format(record)

      try:
         result = requests.post(self.hook_url, json.dumps({"text" : log_entry}), headers={"Content-type": "application/json"}).content

      except:
         print(traceback.format_exc())

      return result
