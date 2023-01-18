from chardet.universaldetector import UniversalDetector


def encoding(doc_path):
    detector = UniversalDetector()
    with open(doc_path, 'rb') as fh:
        for line in fh:
            detector.feed(line)
            if detector.done:
                break
        detector.close()

    return detector.result['encoding']

a = encoding("D:\\Users\\User\Have_to\one\\find\media\\text_f88.txt")
print(a)
