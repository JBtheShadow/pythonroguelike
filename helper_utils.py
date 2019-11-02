def group(options):
    groups = {}
    for option in options:
        if not groups.get(option):
            groups[option] = 0
        groups[option] += 1
    
    return groups

def group_options(options):
    new_options = []
    groups = group(options)
    for key in groups:
        if groups[key] > 1:
            new_options.append('{0} x{1}'.format(key, groups[key]))
        else:
            new_options.append(key)
    
    return new_options
