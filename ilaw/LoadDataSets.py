from logging import Logger


def _load_data(file_name, label_at_last_position=True, ignore_first_line=False, convert_to_float=True):
    # data format :[([a1,a2,a3,...], "label"), ([a1,a2,a3,...], "label"), ...]
    data = []
    with open(file_name) as f:
        i = 0
        for line in f:
            i += 1
            if ignore_first_line and i == 1:
                continue
            params = line.split(",")
            params = [a.strip() for a in params]
            if label_at_last_position:
                label = params.pop(-1)
            else:
                label = params.pop(0)
            if len(params) < 2:  # empty/broken line
                continue
            if convert_to_float:
                data.append(([float(a) for a in params], label))
            else:
                data.append(([a for a in params], label))
    return data


def load_IRIS():
    return _load_data("data/iris.data")


def load_WINE():
    return _load_data("data/wine.data", False)


def load_GLASS():
    return _load_data("data/glass.data")


def load_banknote():
    return _load_data("data/data_banknote_authentication.txt")


def load_weather():
    return _load_data("data/weather.csv", ignore_first_line=True, convert_to_float=False)
