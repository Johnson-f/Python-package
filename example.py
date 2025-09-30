# File describing how you'd import the package on your project

from stonksapi.alpha_vantage import AlphaVantageClient

print("--- Attempting to import AlphaVantageClient from stonksapi.alpha_vantage ---")

print("Successfully imported AlphaVantageClient!")

try:
    # This is expected to fail without an API key set in the environment,
    # but it proves that the class was imported and can be called.
    client = AlphaVantageClient()
    print("Client instantiation works.")
except ValueError as e:
    print(f"As expected, client instantiation failed without an API key: {e}")

print("--- Import test complete. The package structure is correct for users. ---")
