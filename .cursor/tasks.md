[
  {
    "title": "1. Decompile APK",
    "prompt": "I have the `reverse-engineering-assistant` project set up and a file named `MarsPro.apk` in the project root. What is the python command to decompile this APK using the toolkit's `decompile.py` script?"
  },
  {
    "title": "2. Static Analysis - Find API Endpoints",
    "prompt": "Using the code in the newly created `@MarsPro-jadx` directory, perform a global search for common API-related keywords. I'm looking for clues about the API structure. Please search for strings like 'https://', 'api', 'v1', 'v2', 'login', 'token', and 'Authorization' to find potential base URLs and authentication methods."
  },
  {
    "title": "3. Start MITM Network Interception",
    "prompt": "I'm ready for dynamic analysis. What is the command in the `reverse-engineering-assistant` toolkit to start the `mitmproxy` listener for network traffic interception?"
  },
  {
    "title": "4. Create API Documentation Template",
    "prompt": "Generate a markdown template in a file named `API_NOTES.md`. The template should provide a clear structure for documenting the API endpoints I discover. It should include a table with columns for: 'Action', 'HTTP Method', 'Endpoint Path', 'Required Headers', and 'JSON Payload Example'."
  },
  {
    "title": "5. Prototype API Calls in Python",
    "prompt": "Generate a Python script named `test_api.py`. The script should use the `requests` library to validate the API endpoints I found with `mitmproxy`. Include placeholder variables for `API_BASE_URL`, `AUTH_TOKEN`, and `DEVICE_ID`. Create functions like `get_device_status()`, `turn_light_on()`, and `set_brightness(level)` that print the request being made and the server's response."
  },
  {
    "title": "6. Generate Home Assistant Component Boilerplate",
    "prompt": "Generate the boilerplate for a new Home Assistant custom component. The domain should be `mars_hydro`. Create the directory structure `custom_components/mars_hydro/` and populate it with a basic `manifest.json`, and empty `__init__.py`, `config_flow.py`, and `light.py` files. The `manifest.json` should declare the domain, name, and a dependency on the http integration."
  },
  {
    "title": "7. Implement Home Assistant Config Flow",
    "prompt": "In the `@custom_components/mars_hydro/config_flow.py` file, create a complete `MarsHydroConfigFlow` class. It should present a form to the user asking for `username` and `password`. On submission, it should have a placeholder async function `_validate_input` that I can later fill in to call the login API endpoint. For now, assume validation is successful. Upon success, it should create the config entry, storing the username and a placeholder API token like `mock_token_12345`."
  },
  {
    "title": "8. Implement Home Assistant Light Entity",
    "prompt": "In the `@custom_components/mars_hydro/light.py` file, generate a complete `MarsHydroLight` entity class that inherits from `LightEntity`. It must:\n1. Use `aiohttp` for all API calls via the `hass.helpers.aiohttp_client` session.\n2. Implement `async_turn_on` and `async_turn_off` by sending a POST request to a placeholder control endpoint like `https://api.marspro.com/v1/device/control`. The payload should be `{\"deviceId\": self._device_id, \"command\": {\"power\": \"on\"}}` or `\"off\"`.\n3. Support brightness by accepting `**kwargs` in `async_turn_on`, checking for `ATTR_BRIGHTNESS`, and sending a payload like `{\"command\": {\"brightness\": <value>}}`.\n4. Define the `supported_color_modes` property to include `brightness`.\n5. Include an `async_update` method to fetch the light's current state from a placeholder status endpoint.\n6. Assume the API token and device ID are passed into the entity's `__init__` method from the config entry."
  },
  {
    "title": "9. Advanced - Frida SSL Unpinning Command",
    "prompt": "I'm not seeing any HTTPS traffic in `mitmproxy`, so I suspect the MarsPro app uses SSL Pinning. Using the `reverse-engineering-assistant` toolkit, what is the full `frida` command to attach to a running application and inject a universal SSL unpinning script? Use `<com.marspro.app>` as a placeholder for the app's package name."
  }
]