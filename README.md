# Enigma Machine

This project is a Python implementation of the classic Enigma Machine, used for encryption and decryption during World War II. The simulator models the main components of the Enigma: Plugboard, Rotors, and Reflector, and allows for customizable settings to encode and decode messages.

## Features

- **`Plugboard`**: Simulates letter pair swaps before and after the rotor process.
- **`Rotors`**: Models the internal wiring, ring settings, and notches for stepping and double-stepping behavior.
- **`Reflector`**: Implements fixed, bidirectional substitution.
- **`Full Enigma Simulation`**: Combines all components to encrypt and decrypt messages, supporting custom rotor types, positions, ring settings, plugboard connections, and reflector types.
- **`Non-alphabetic Characters`**: Non-letter characters (spaces, numbers, punctuation) are preserved in the output.

## Usage

Run the script directly to see example encryptions and decryptions:

```bash
python3 main.py
```

## Customization

You can change the Enigma settings by modifying the parameters in the `Enigma` class instantiation:

- `rotor_types`: List of rotor types (e.g., `["I", "II", "III"]`).
- `rotor_settings`: Initial rotor positions (e.g., `"ABC"`).
- `ring_settings`: Ring settings for each rotor (e.g., `"AAA"`).
- `plugboard_settings`: Plugboard connections (e.g., `"AZ BS"`).
- `reflector_type`: Reflector type (e.g., `"B"`).

## Code Structure

- `Plugboard`: Handles letter swaps.
- `Rotor`: Models rotor wiring, position, ring setting, and stepping.
- `Reflector`: Handles signal reflection.
- `Enigma`: Orchestrates the encryption/decryption process.

## Requirements

- Python 3.x
- No external dependencies

## License

This project is provided for educational purposes and is released under the MIT License.
