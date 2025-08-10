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
