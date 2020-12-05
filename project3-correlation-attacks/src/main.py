from tqdm import tqdm
from dataclasses import dataclass
import matplotlib.pyplot as plt


with open("input_sequence.txt", "r") as seq:
    encrypted_sequence = [int(x) for x in seq.readline()]


@dataclass
class Sequence:
    """Class for storing info about a given sequence"""

    sequence: list[int]
    similarity: float
    initial_state: list[int]


def lfsr(polynomial, initial_state, base, length):

    # linear behaviour - logic borrowed from project 2
    internal_register = initial_state.copy()
    sequence = []
    for i in range(length):
        new_register_value = 0
        for coefficient, content in zip(polynomial, internal_register):
            new_register_value += -coefficient * content

        internal_register.append(new_register_value % base)
        sequence.append(internal_register.pop(0))

    return sequence


def correlation(sequence1, sequence2):
    differing_positions = 0
    for sequence1_digit, sequence2_digit in zip(sequence1, sequence2):
        if sequence1_digit != sequence2_digit:
            differing_positions += 1
    return 1 - differing_positions / len(sequence1)


def get_possible_sequences(polynomial):
    sequences = []
    for i in tqdm(range(2 ** len(polynomial))):
        # Convert to binary with polynomial length digits, and then to int,
        # and save it on a list
        initial_state = [int(x) for x in format(i, f"0{len(polynomial)}b")]

        sequence = lfsr(polynomial, initial_state, 2, len(encrypted_sequence))
        similarity = abs(correlation(sequence, encrypted_sequence))

        sequences.append(Sequence(sequence, similarity, initial_state))

    return sequences


def plot_sequences(sequences, max, state, max_index, number):
    x_coordinates = list(range(len(sequences)))
    y_coordinates = [sequence.similarity for sequence in sequences]

    plt.scatter(x_coordinates, y_coordinates)
    plt.annotate(
        f"({state}, {max})",
        xy=(max_index, max),
        xytext=(max_index / 2, max - 0.05),
        ha="center",
        arrowprops=dict(arrowstyle="->", lw=1),
    )
    plt.savefig(f"lfsr_{number}.png")
    plt.close()


def validate(generated_sequences, states):
    generated_keystream = []

    print("Verifying combined LFSR sequence...")
    for output_symbol1, output_symbol2, output_symbol3 in zip(
        generated_sequences[0], generated_sequences[1], generated_sequences[2]
    ):
        outputs = [output_symbol1, output_symbol2, output_symbol3]
        if outputs.count(1) <= 1:
            generated_keystream.append(0)
        else:
            generated_keystream.append(1)

    if generated_keystream == encrypted_sequence:
        print("Generated sequence is equal to given sequence! Keys are: ")
        for s in states:
            print(str(s))
        return True
    else:
        print(
            "Could not generate an equal sequence. Closest was the following sequence and keys:"
        )
        print("    * Sequence: " + str(generated_keystream))
        print("    * Keys: " + str(states))

        return False


def main():

    # Coefficients - left is higher exponent
    connection_polynomials = [
        [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0],
    ]

    states = []
    generated_sequences = []
    plot = False

    for index, polynomial in enumerate(connection_polynomials):
        print(f"\nGenerating all sequences for polynomial {polynomial}")
        sequences = get_possible_sequences(polynomial)

        # Find sequence with higher correlation with the encrypted sequence
        most_similar_sequence = max(sequences, key=lambda s: s.similarity)

        if plot:
            plot_sequences(
                sequences,
                round(most_similar_sequence.similarity, 3),
                most_similar_sequence.initial_state,
                sequences.index(most_similar_sequence),
                index,
            )

        # Save the "best" sequence, and the initial state that leads to it
        generated_sequences.append(most_similar_sequence.sequence)
        states.append(most_similar_sequence.initial_state)

    # Verify that this generates the provided keystream
    validate(generated_sequences, states)


main()
