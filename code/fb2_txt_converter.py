import os
from bs4 import BeautifulSoup


def convert_fb2_to_txt(input_path, output_path):
    '''
    FB2 to TXT converter

    Args:
    input_path (str): Str of input path name.
    output_path (str): Str of output path name.

    Returns:
    bool
    '''
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'xml')

        text_parts = []

        for body in soup.find_all('body'):
            for section in body.find_all('section'):
                section_text = []

                for title in section.find_all('title'):
                    text = title.get_text().strip()
                    if text:
                        section_text.append(text)

                for elem in section.find_all(['p', 'subtitle']):
                    text = elem.get_text().strip()
                    if text:
                        section_text.append(text)

                if section_text:
                    text_parts.append('\n\n'.join(section_text))

        if not text_parts:
            for p in soup.find_all('p'):
                text = p.get_text().strip()
                if text:
                    text_parts.append(text)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(text_parts))

        return True

    except Exception as e:
        print(f"🚨 Conversion error {os.path.basename(input_path)}: {str(e)}")
        return False
