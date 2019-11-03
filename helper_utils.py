def group(options):
    groups = {}
    for option in options:
        if not groups.get(option):
            groups[option] = {"count": 0, "index": options.index(option)}
        groups[option]["count"] += 1
    
    return groups


def group_options(options):
    new_options = []
    groups = group(options)
    for key in groups:
        if groups[key]["count"] > 1:
            new_options.append('{0} x{1}'.format(key, groups[key]["count"]))
        else:
            new_options.append(key)
    
    return new_options


def group_indexes(options):
    groups = group(options)
    return [groups[key]["index"] for key in groups]
