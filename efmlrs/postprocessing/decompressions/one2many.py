from fractions import Fraction


def parse_info(file):
    iterations = []
    tmp = []
    post = 0
    pre = 0
    for line in file:

        if line.startswith("merged"):
            tokens = line.strip().split()
            post, pre = tokens[1].split(":")

        if line.startswith("remove"):
            infos = []

            for i in line.strip().split():
                if i == "remove" or i == "keep":
                    continue
                tokens = i.split(":")
                if len(tokens) <= 1:
                    continue
                index = int(tokens[0][1:])
                factor = Fraction(tokens[1])
                infos.append((index, factor))
            iterations.append(infos)
        if line.startswith("end"):
            break

    tmp.append(iterations[::-1])
    tmp.append(int(post))
    tmp.append(int(pre))
    return iterations[::-1], int(post), int(pre)


def build_merge_mapping(iterations, post):
    insertions = []
    for i in iterations:
        index = i[0][0]
        insertions.append(index)
    insertions = sorted(insertions)
    mapping = {}
    count = 0
    for i in range(0, post):
        if i in insertions:
            continue
        mapping[count] = i
        count += 1
    return mapping


def demerge(efms_fileName, output_fileName, mapping, iterations, post_len):
    print(efms_fileName)
    input = open(efms_fileName, "r")
    output = open(output_fileName, "w")

    for line in input:
        compressed = line.strip().split()
        target = [None] * post_len

        for i in range(0, len(compressed)):
            target[mapping[i]] = Fraction(compressed[i])

        for iter in iterations:
            merged_index, merged_factor = iter[0]
            total = 0
            for index, factor in iter[1:]:
                total += target[index]
            target[merged_index] = total / merged_factor

            for index, factor in iter[1:]:
                target[index] /= factor

        for i in target:
            output.write(str(float(i)) + " ")
        output.write("\n")
    input.close()
    output.close()


def decompressions(cmp_efm, mapping, iterations, post):
    target = [None] * post
    for i in range(0, len(cmp_efm)):
        target[mapping[i]] = cmp_efm[i]

    for it in iterations:
        merged_index, merged_factor = it[0]
        total = 0

        for index, factor in it[1:]:
            total += target[index]
        target[merged_index] = total / merged_factor

        for index, factor in it[1:]:
            target[index] /= factor

    return target
