import string

class Plugboard:
    """
    Simulates the Enigma Machine's Plugboard.
    Performs swaps of letter pairs.
    """
    def __init__(self, mappings):
        """
        Initializes the Plugboard with cable mappings.
        Example: "AZ BS" means 'A' swaps with 'Z' and 'B' with 'S'.
        The mappings are stored as indices (0-25).
        """
        self.alphabet = string.ascii_uppercase
        self.mapping = list(range(26))

        for pair in mappings.split():
            if len(pair) == 2:
                char1_idx = self.alphabet.find(pair[0].upper())
                char2_idx = self.alphabet.find(pair[1].upper())
                self.mapping[char1_idx] = char2_idx
                self.mapping[char2_idx] = char1_idx

    def process(self, char_index):
        """
        Processes a letter index through the Plugboard.
        :param char_index: Input letter index (0-25).
        :return: Output letter index (0-25) after swapping.
        """
        return self.mapping[char_index]


class Rotor:
    """
    Simulates an Enigma Machine Rotor.
    Each rotor has internal wiring, a ring setting, and a notch that triggers the next rotor.
    """
    def __init__(self, wiring, notch, ring_setting=0):
        """
        Initializes a rotor.
        :param wiring: String defining the internal wiring (e.g., "EKMFLGDQVZNTOWYHXUSPAIBRCJ").
                       Position 'A' maps to the first letter, 'B' to the second, etc.
        :param notch: Notch character that causes the left rotor to step (e.g., 'Q').
                      This is the point on the rotor ring that triggers the next rotor.
        :param ring_setting: Ring setting position (0-25, where 0 is 'A'). Adjusts the internal wiring
                             relative to the visible rotor position.
        """
        self.alphabet = string.ascii_uppercase
        self.wiring = wiring
        self.notch = notch.upper()
        self.position = 0
        self.ring_setting = ring_setting

    def rotate(self):
        """Rotates the rotor by one position."""
        self.position = (self.position + 1) % 26

    def at_notch(self):
        """
        Checks if the rotor is at the notch position.
        The notch condition is based on the letter visible in the rotor window (self.position).
        """
        return self.alphabet[self.position] == self.notch

    def process_forward(self, char_index):
        """
        Processes a letter index through the rotor in the forward direction (right to left).
        Adjusts input and output based on the current rotor position and ring setting.
        :param char_index: Input letter index (0-25).
        :return: Output letter index (0-25).
        """
        input_to_rotor_body = (char_index + self.position) % 26
        input_to_wiring_index = (input_to_rotor_body - self.ring_setting + 26) % 26
        output_from_wiring_char = self.wiring[input_to_wiring_index]
        output_from_wiring_index = self.alphabet.find(output_from_wiring_char)
        output_index_after_ring = (output_from_wiring_index + self.ring_setting) % 26
        final_output_index = (output_index_after_ring - self.position + 26) % 26
        return final_output_index

    def process_backward(self, char_index):
        """
        Processes a letter index through the rotor in the backward direction (left to right).
        Adjusts input and output based on the current rotor position and ring setting.
        :param char_index: Input letter index (0-25).
        :return: Output letter index (0-25).
        """
        input_to_rotor_body = (char_index + self.position) % 26
        input_to_wiring_index = (input_to_rotor_body - self.ring_setting + 26) % 26
        output_from_wiring_index = self.wiring.find(self.alphabet[input_to_wiring_index])
        output_index_after_ring = (output_from_wiring_index + self.ring_setting) % 26
        final_output_index = (output_index_after_ring - self.position + 26) % 26
        return final_output_index


class Reflector:
    """
    Simulates the Enigma Machine's Reflector (Umkehrwalze).
    Performs a fixed, bidirectional substitution, sending the signal back through the rotors.
    """
    def __init__(self, wiring):
        """
        Initializes the Reflector with its wiring.
        :param wiring: String defining the wiring (e.g., "YRUHQSLDPXNGOKMIEBFZCWVJAT").
                       'A' maps to the first letter, 'B' to the second, etc.
        The mappings are stored as indices (0-25).
        """
        self.alphabet = string.ascii_uppercase
        self.mapping = [self.alphabet.find(c) for c in wiring]

    def reflect(self, char_index):
        """
        Reflects a letter index.
        :param char_index: Input letter index (0-25).
        :return: Output letter index (0-25) after reflection.
        """
        return self.mapping[char_index]


class Enigma:
    """
    Simulates the complete Enigma Machine.
    Combines Plugboard, Rotors, and Reflector to encrypt/decrypt messages.
    """
    ROTOR_WIRINGS = {
        "I":   "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch_I": "Q",
        "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch_II": "E",
        "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch_III": "V",
        "IV":  "ESOVPZJAYQUIRHXLNFTGKDCMWB", "notch_IV": "J",
        "V":   "VZBRGITYUPSDNHLXAWMJQOFECK", "notch_V": "Z"
    }

    REFLECTOR_WIRINGS = {
        "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    }

    def __init__(self, rotor_types, rotor_settings, ring_settings, plugboard_settings, reflector_type):
        """
        Initializes the Enigma Machine.
        :param rotor_types: List of strings with rotor types (e.g., ["I", "II", "III"]).
                            Should be provided left to right (slow to fast rotor).
        :param rotor_settings: String with initial rotor positions (e.g., "ABC").
                               Each character corresponds to the letter visible in the rotor window.
        :param ring_settings: String with ring settings for the rotors (e.g., "AAA").
                              Each character defines the ring offset for the corresponding rotor.
        :param plugboard_settings: String with plugboard connections (e.g., "AZ BS").
        :param reflector_type: String with the reflector type (e.g., "B").
        """
        self.alphabet = string.ascii_uppercase
        self.plugboard = Plugboard(plugboard_settings)
        self.reflector = Reflector(self.REFLECTOR_WIRINGS[reflector_type.upper()])

        self.rotors = []
        for i, rotor_type in enumerate(rotor_types):
            rotor_wiring = self.ROTOR_WIRINGS[rotor_type.upper()]
            rotor_notch = self.ROTOR_WIRINGS[f"notch_{rotor_type.upper()}"]
            ring_setting_char = ring_settings[i].upper()
            ring_setting_int = self.alphabet.find(ring_setting_char)
            rotor = Rotor(rotor_wiring, rotor_notch, ring_setting_int)
            rotor.position = self.alphabet.find(rotor_settings[i].upper())
            self.rotors.append(rotor)

        if len(self.rotors) >= 3:
            self.slow_rotor = self.rotors[0]
            self.medium_rotor = self.rotors[1]
            self.fast_rotor = self.rotors[2]
        else:
            raise ValueError("The Enigma Machine requires at least 3 rotors for this simulation.")

    def _step_rotors(self):
        """
        Controls rotor movement before each character is encrypted.
        Implements the Enigma I "stepping" and "double-stepping" mechanism.
        """
        if self.medium_rotor.at_notch():
            self.medium_rotor.rotate()
            self.slow_rotor.rotate()
        elif self.fast_rotor.at_notch():
            self.medium_rotor.rotate()
        self.fast_rotor.rotate()

    def encrypt_char(self, char):
        """
        Encrypts/decrypts a single character.
        """
        char = char.upper()
        if not char.isalpha():
            return char

        self._step_rotors()

        char_index = self.alphabet.find(char)
        processed_index = self.plugboard.process(char_index)
        for rotor in reversed(self.rotors):
            processed_index = rotor.process_forward(processed_index)
        processed_index = self.reflector.reflect(processed_index)
        for rotor in self.rotors:
            processed_index = rotor.process_backward(processed_index)
        final_index = self.plugboard.process(processed_index)
        return self.alphabet[final_index]

    def encrypt_message(self, message):
        """
        Encrypts/decrypts a complete message.
        """
        encrypted_message = ""
        for char in message:
            encrypted_message += self.encrypt_char(char)
        return encrypted_message
