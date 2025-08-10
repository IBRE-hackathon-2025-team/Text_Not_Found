def kcreator(string, k):
    list_of_Kmer = []
    for i in range(0, len(string) - k + 1):
        frame = string[i : i + k]
        list_of_Kmer.append(frame)

    return list_of_Kmer


def kcounter(from_list):
    to_dict = {}
    for i in from_list:
        if i in to_dict:
            to_dict[i] += 1
        else:
            to_dict[i] = 1

    return to_dict