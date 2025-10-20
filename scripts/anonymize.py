# python ./scripts/anonymize.py -i ./input -o ./anonymized

from pathlib import Path
import re
import xml.etree.ElementTree as ET

anonymize_attributes = [
    "testobject_name",
    "project_name",
    "module_name",
    "testobject_name",
    #"decl",
    #"nam",
    #"text",
    #"type",
    "name",
    #"value",
]

empty_attributes = [
    "host",
    "user",
]

empty_tags = [
    "properties",
    "interface",
    "interfaceReport",
    "inputs",
    "results",
    "prologs_epilogs",
    "usercode",
    "coverage",
]

def anonymize_text(text: str) -> str:
    """
    Anonymizes the given text by replacing its content with a anonymized text
    matching the length and structure.

    :param text: The original text to be anonymized.
    :return: The anonymized text.
    """
    text_out = re.sub(r'[a-z]', 'x', text)
    text_out = re.sub(r'[A-Z]', 'X', text_out)
    text_out = re.sub(r'[0-9]', '0', text_out)
    return text_out

def anonymize_ET(element):
    for att in element.attrib:
        if att in anonymize_attributes:
            element.attrib[att] = anonymize_text(element.attrib[att])
        if att in empty_attributes:
            element.attrib[att] = ""

    for child in element:
        if child.tag in empty_tags:
            child.clear()
        else:
            child = anonymize_ET(child)

    return element


def anonymize_xml_content(text: str) -> str:
    """
    Anonymizes the content of an XML file by user attributes with anonymized content.

    :param text: The original XML content.
    :return: The anonymized XML content.
    """

    # translate text to xml structure
    root = ET.fromstring(text)

    root = anonymize_ET(root)

    # xml structure to string
    return ET.tostring(root, encoding="utf-8").decode("utf-8")

def anonymize_folder(input_folder: Path, output_folder: Path) -> None:
    """
    Anonymizes all .xml files in the input_folder by replacing their content with a placeholder
    and saves them to the output_folder.

    :param input_folder: Path to the folder containing files to be anonymized.
    :param output_folder: Path to the folder where anonymized files will be saved.
    """
    if not input_folder.is_dir():
        print(f"Error: The input folder '{input_folder}' does not exist or is not a directory.")
        return

    for file_path in input_folder.glob("*.xml"):
        print(f"Anonymizing file: {file_path.absolute()}")
        try:
            # read unicode file content
            with file_path.absolute().open("r", ) as f_in: #encoding="utf-8"
                text = f_in.read()

            text_anonymized = anonymize_xml_content(text)

            output_file_path = output_folder / file_path.name
            output_file_path.write_text(text_anonymized)
            print(f"Anonymized file saved to: {output_file_path}")
        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")

def main():
      import argparse

      parser = argparse.ArgumentParser(description="Anonymize XML files in a folder.")
      parser.add_argument("-i", "--input_folder", help="Path to the input folder containing XML files.", required=True, type=Path)
      parser.add_argument("-o", "--output_folder", help="Path to the output folder for anonymized XML files.", required=True, type=Path)

      args = parser.parse_args()

      anonymize_folder(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
