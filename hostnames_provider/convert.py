csv_file = request.FILES['filename'].name
txt_file = 'dados.txt'

text_list = []

with open(csv_file, "r") as my_input_file:
    for line in my_input_file:
        line = line.split(",", 2)
        text_list.append(" ".join(line))

with open(txt_file, "w") as my_output_file:
    for line in text_list:
        my_output_file.write(line)
    print('File Successfully written.')
