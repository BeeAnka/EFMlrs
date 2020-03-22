from fractions import Fraction


def parse_info(file):
    cmp_infos = []
    for line in file:
        if line.startswith("R"):
            infos = {}
            data = line.strip().split()
            for i in data:
                tokens = i.split(",")
                if len(tokens) <= 1:
                    continue
                index_1 = tokens[0][1:]
                index_2, factor = tokens[1].split(":")
                infos[int(index_1)] = (int(index_2), Fraction(factor))
            cmp_infos.append((infos, len(data), len(data) + len(infos)))
        if line.startswith("end"):
            break
    return cmp_infos


def build_mapping(infos, rea_uncomp):
    mapping = {}

    for index_1, value in infos.items():
        index_2, factor = value
        mapping[index_2] = (index_1, Fraction(factor))

    count = 0
    for i in range(0, rea_uncomp):
        if i in mapping:
            continue
        mapping[i] = count
        count += 1

    mapping = sorted(mapping.items())
    return mapping


def uncompress(efms_filename, output_filename, mapping):
    print(efms_filename)
    input = open(efms_filename, "r")
    output = open(output_filename, "w")

    for line in input:
        compressed = line.strip().split()

        for i, val in mapping:
            if type(val) == int:
                output.write(compressed[val])
            else:
                index = val[0]
                factor = val[1]
                output.write(str(Fraction(compressed[index]) * factor))
            output.write(" ")
        output.write("\n")
    input.close()
    output.close()


def decompressions(cmp_efm, mapping):
    target = []
    for i, val in mapping:
        if type(val) == int:
            target.append(cmp_efm[val])
        else:
            index = val[0]
            factor = val[1]
            mapped_index = mapping[index][1]
            new_val = Fraction(cmp_efm[mapped_index]) / factor
            target.append(new_val)
    return target
