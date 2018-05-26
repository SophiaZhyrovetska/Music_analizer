def right_name(line):
    """
    Returns enterd name in right format
    :param line: str
    :return: list
    """
    a = line.find(",")
    b = line.find(";")
    if a == -1 and b == -1:
        return [line, '']
    if a != -1:
        return [i.strip() for i in line.split(",")]
    return [i.strip() for i in line.split(";")]

