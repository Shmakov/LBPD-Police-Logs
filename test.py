import PyPDF2
import re
import os
import csv


def get_text(filename):
    """
    Get text content out of PDF file
    :param filename: str
    :return: str
    """
    result = ''

    pdf_file = open(filename, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = pdf_reader.getNumPages()
    for i in range(0, number_of_pages):
        page = pdf_reader.getPage(i)
        result = result + page.extractText()

    # Below fixes bug with new lines in between word(s)
    result = re.sub('([A-Za-z0-9\-_:/#]+)\n([A-Za-z0-9\-_:/#]+)', r'\1\2', result)
    result = re.sub('([A-Za-z0-9\-_:/#]+)\n([A-Za-z0-9\-_:/#]+)', r'\1\2', result)
    return result


def parse_text(text):
    """
    Parses text and returns list of dictionaries
    :param text: str
    :return: list
    """
    result = []

    events = re.split('__+', text)
    for event_text in events:
        if "Event #" in event_text:
            match = re.match('\s*Event\s+#\s+(?P<name>.+?)$'
                             '\s+Type\s+(?P<type_code>.+?)\s+'
                             '(?P<type>.+?)$'
                             '.*?(?P<date>[0-9]+/[0-9]+/[0-9]+\s+[0-9]+:[0-9]+:[0-9]+)'
                             '.+?^Subtype\s+(?!Disposition)(?P<sub_type>.*?)$'
                             '.+?^Disposition\s+(?!Descript\.)(?P<disposition>.*?)$'
                             '.+?^Descript\.\s+(?!Location)(?P<description>.*?)$'
                             '.+?^Location(\s+)?(?P<location>.*)$', event_text, re.MULTILINE | re.DOTALL)
            if match:
                name = re.sub('\n+', '', match.group('name')).strip()
                type_code = re.sub('\n+', '', match.group('type_code')).strip()
                type = re.sub('\n+', '', match.group('type')).strip()
                sub_type = re.sub('\n+', '', match.group('sub_type')).strip()
                disposition = re.sub('\n+', '', match.group('disposition')).strip()
                description = re.sub('\n+', '', match.group('description')).strip()
                location = re.sub('\n+', '', match.group('location')).strip()
                date = re.sub('\s+', ' ', match.group('date')).strip()
                event = {'name': name, 'type_code': type_code, 'type': type, 'sub_type': sub_type,
                         'disposition': disposition, 'description': description, 'location': location, 'date': date}
                result.append(event)

    return result


def export_to_csv(data, filename):
    """
    Export data to csv file
    :param data: list
    :param filename: str
    """
    keys = data[0].keys()
    with open(filename, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, keys)
        writer.writeheader()
        writer.writerows(data)


# data = parse_text(get_text('pdf_logs/2018_11_17.pdf'))
# print(data)
# print(get_text('pdf_logs/2018_10_17.pdf'))
# export_to_csv(data, 'test.csv')

if __name__ == '__main__':
    current_path = os.path.dirname(os.path.realpath(__file__))
    pdf_logs_path = current_path + "/pdf_logs/"

    data = []
    for filename in os.listdir(pdf_logs_path):
        if filename.endswith(".pdf"): #2019_6_17
            text_content = get_text(pdf_logs_path + '/' + filename)
            data = data + parse_text(text_content)
    export_to_csv(data, 'test.csv')