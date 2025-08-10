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
