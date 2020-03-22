def parse_info(file):
    cmp_infos = []
    for line in file:
        if line.startswith("remove"):
            reactions = []
            for rea in line.split()[1:]:
                reactions.append(int(rea))
            cmp_infos.append(reactions)
        if line.startswith("end"):
            break
    return cmp_infos


def decompressions(compressed, mapping):
    [compressed.insert(val, 0) for val in mapping]
    return compressed
