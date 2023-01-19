def read_txt(doc_path, encod):
    with open(doc_path, 'r', encoding=encod) as txt:
        line_count = 1
        for line in txt:
            line = line.strip()
            print(line)
            words = line.replace('\t', '') \
                .replace('\n', '') \
                .replace('.', '') \
                .replace(',', '') \
                .replace('!', '') \
                .replace('?', '') \
                .replace('  ', ' ').split(' ')
            #print(words)
        line_count += 1


read_txt('D:\\Users\\User\Have_to\one\\find\media\day3_mVweORE.txt', 'utf-8')