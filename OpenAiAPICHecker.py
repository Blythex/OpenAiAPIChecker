import openai
from colorama import Fore, Style
import concurrent.futures
import time
import sys

def check_gpt3_api_key(api_key):
    openai.api_key = api_key

    # Beispielanfrage an die API, um die Gültigkeit des API-Schlüssels zu überprüfen
    prompt = "This is a test prompt."
    try:
        response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=5)
        return True  # API-Schlüssel ist gültig
    except openai.error.RateLimitError:
        return "LIMIT_EXPECTED"  # API-Schlüssel hat das erwartete Limit
    except openai.error.AuthenticationError:
        return False  # API-Schlüssel ist ungültig

def check_api_keys(api_keys):
    valid_keys = []
    limit_expected_keys = []
    invalid_keys = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Prüfe die API-Schlüssel parallel
        results = {executor.submit(check_gpt3_api_key, key.strip()): key.strip() for key in api_keys}

        for future in concurrent.futures.as_completed(results):
            key = results[future]
            try:
                result = future.result()
                if result is True:
                    sys.stdout.write(f"\r{Fore.GREEN}Valid API key: {key}{Style.RESET_ALL}")
                    valid_keys.append(key)
                elif result == "LIMIT_EXPECTED":
                    sys.stdout.write(f"\r{Fore.BLUE}API key with expected limit: {key}{Style.RESET_ALL}")
                    limit_expected_keys.append(key)
                else:
                    sys.stdout.write(f"\r{Fore.RED}Invalid API key: {key}{Style.RESET_ALL}")
                    invalid_keys.append(key)
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(f"\r{Fore.RED}Error checking API key: {key}. Error: {e}{Style.RESET_ALL}")
                sys.stdout.flush()
                invalid_keys.append(key)

    return valid_keys, limit_expected_keys, invalid_keys

def main():
    # Text für Spenden-Nachricht
    donations_text = "DONATIONS BTC TO : bc1qtkxuklcps9tf8hmgy8l62f5k8h3v2myduea68k"
    print(donations_text)

    with open("api.txt", "r") as file:
        api_keys = file.readlines()

    start_time = time.time()  # Startzeitpunkt der Überprüfung

    valid_keys, limit_expected_keys, invalid_keys = check_api_keys(api_keys)

    end_time = time.time()  # Endzeitpunkt der Überprüfung
    total_time = end_time - start_time  # Gesamtdauer der Überprüfung in Sekunden

    with open("valid_api_keys.txt", "w") as valid_file:
        valid_file.write("\n".join(valid_keys))

    with open("limit_expected_api_keys.txt", "w") as limit_expected_file:
        limit_expected_file.write("\n".join(limit_expected_keys))

    with open("invalid_api_keys.txt", "w") as invalid_file:
        invalid_file.write("\n".join(invalid_keys))

    # Anzahl der geprüften API-Schlüssel
    total_keys = len(api_keys)
    # Anzahl der gültigen API-Schlüssel
    valid_count = len(valid_keys)
    # Anzahl der API-Schlüssel mit erwartetem Limit
    limit_expected_count = len(limit_expected_keys)
    # Anzahl der ungültigen API-Schlüssel
    invalid_count = len(invalid_keys)

    print("\n")
    print(f"Checked {total_keys} API keys.")
    print(f"{valid_count} valid API keys.")
    print(f"{limit_expected_count} API keys with expected limit.")
    print(f"{invalid_count} invalid API keys.")
    print(f"Total time taken: {total_time:.2f} seconds.")  # Gesamtdauer in Sekunden ausgeben

if __name__ == "__main__":
    main()