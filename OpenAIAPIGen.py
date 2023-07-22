import secrets
import string

def generate_api_key():
    # Länge des alphanumerischen Teils des Schlüssels
    key_length = 48  # 50 Zeichen abzüglich 2 für "sk" Präfix

    # Zeichen, die im Schlüssel enthalten sein sollen (erweiterte Zeichenpalette ohne Bindestrich und Unterstrich)
    characters = string.ascii_letters + string.digits

    # Generiere den zufälligen alphanumerischen Teil des Schlüssels
    random_part = ''.join(secrets.choice(characters) for _ in range(key_length))

    # Füge das Präfix hinzu
    api_key = "sk-" + random_part
    return api_key

def save_api_keys_to_file(api_keys, filename):
    with open(filename, "w") as file:
        for api_key in api_keys:
            file.write(api_key + "\n")

if __name__ == "__main__":
    try:
        num_keys = int(input("Geben Sie die Anzahl der zu generierenden API-Schlüssel ein: "))
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")
    else:
        if num_keys <= 0:
            print("Die Anzahl der zu generierenden API-Schlüssel muss größer als 0 sein.")
        else:
            # Generiere die API-Schlüssel
            api_keys = [generate_api_key() for _ in range(num_keys)]

            # Speichere die API-Schlüssel in api.txt
            save_api_keys_to_file(api_keys, "api.txt")

            print(f"{num_keys} API-Schlüssel wurden in api.txt gespeichert.")
