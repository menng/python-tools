# -*- coding: utf-8 -*-

import requests

response = requests.get("https://gitlab.com/api/v4/projects?private_token=xx")
print response.status_code