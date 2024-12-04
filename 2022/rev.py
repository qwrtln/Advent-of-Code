from string import ascii_lowercase

a = "abc&fd,vw"


def reverse_non_special(string: str):
    special_positions = {}
    normal_positions = {}
    for index, character in enumerate(string):
        if character in ascii_lowercase:
            normal_positions[index] = character
        else:
            special_positions[index] = character

    normal_reversed = list(normal_positions.values())[::-1]
    output = ""
    for i in range(len(string)):
        if i in special_positions:
            output += special_positions[i]
        else:
            output += normal_reversed[i]
    return output


reverse_non_special(a)
