def parse(input_text, array):

    while True:
        data = input_text.readline()
        if data:
            if data[len(data) - 1] is '\n':
                data = data[:len(data) - 1]

            if data is '':
                continue

            array.append(data)
        else:
            break