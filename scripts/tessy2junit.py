# python ./scripts/tessy2junit.py -i ./anonymized -o ./output

from pathlib import Path
import re
import xml.etree.ElementTree as ET

class testcase:
    def __init__(self, classname: str, name: str, uuid: str, time: float = 0.0):
        self.classname = classname
        self.name = name
        self.time = time
        self.uuid = uuid
        self.attributes = {
            "classname": classname,
            "name": name,
            "time": time
        }
        self.children = []

    def set_attribute(self, key: str, value):
        self.attributes[key] = value

    def add_child(self, child):
        self.children.append(child)

    def to_element(self):
        element = ET.Element("testcase", {k: str(v) for k, v in self.attributes.items()})
        for child in self.children:
            element.append(child.to_element())
        return element

class testsuite:
    def __init__(self, name: str, uuid: str, errors: int = 0, failures: int = 0, skipped: int = 0, tests: int = 0, time: float = 0.0, timestamp: str = "", hostname: str = ""):
        self.name = name
        self.uuid = uuid
        self.errors = errors
        self.failures = failures
        self.skipped = skipped
        self.tests = tests
        self.time = time
        self.timestamp = timestamp
        self.attributes = {
            "name": name,
            "errors": errors,
            "failures": failures,
            "skipped": skipped,
            "tests": tests,
            "time": time,
            "timestamp": timestamp,
            "hostname": hostname
        }
        self.children = []

    def set_attribute(self, key: str, value):
        self.attributes[key] = value

    def add_child(self, child):
        self.children.append(child)

    def to_element(self):
        element = ET.Element("testsuite", {k: str(v) for k, v in self.attributes.items()})
        for child in self.children:
            element.append(child.to_element())
        return element

class testsuites:
    def __init__(self, name: str):
        self.name = name
        self.attributes = {
            "name": name,
        }
        self.children = []

    def set_attribute(self, key: str, value):
        self.attributes[key] = value

    def add_testsuite(self, testsuite):
        self.children.append(testsuite)

    def to_element(self):
        element = ET.Element("testsuites", {k: str(v) for k, v in self.attributes.items()})
        for child in self.children:
            element.append(child.to_element())
        return element

"""

testsuites name
"tessy tests"


testsuite name="pytest"
info project_name

testsuite errors="0"
statistic notok="0"

testsuite failures="0"
--

testsuite skipped="0"
statistic notexecuted="0"

testsuite tests="8"
statistic total="5"

testsuite time="0.073"
--

testsuite timestamp="2025-10-07T15:17:26.722982+00:00"
info date="2024-11-26" info time="13:08:11+0100"

testsuite hostname="runnervmwhb2z"
info host=""



testcase classname="tests.merge_dicts_test.Test_Merge_Dicts"
testcase prologs_epilogs <prolog type="source" text=""/>

testcase name="test_merge_dictionaries"
testcase name

testcase time="0.001"
--
"""
def tessy2junit_testcase(tessy_elements) -> testcase:
    if tessy_elements.tag != "testcase":
        return None

    new_testcase = testcase(
         classname = "",
         name = tessy_elements.attrib.get("name", ""),
         uuid = tessy_elements.attrib.get("uuid", ""),
         time = 0.0,
    )
    return new_testcase


def tessy2junit_testsuite(tessy_element, junit_element: testsuites) -> testsuites:

    if tessy_element.tag == "report":
        summary = tessy_element.find("summary")
        if summary is not None:
            info = summary.find("info")
            if info is None:
                print("missing info in summary")
                return junit_element
            project_name = info.attrib.get("project_name", "unknown_project")
            module_name = info.attrib.get("module_name", "unknown_module")
            module_uuid = info.attrib.get("module_uuid", "unknown_uuid")
            date = info.attrib.get("date", "")
            time = info.attrib.get("time", "")
            host = info.attrib.get("host", "")
        else:
            #todo handle missing summary
            print("missing summary in report")
            return junit_element

        statistic = summary.find("statistic")
        if statistic is not None:
            total = int(statistic.attrib.get("total", "0"))
            notok = int(statistic.attrib.get("notok", "0"))
            notexecuted = int(statistic.attrib.get("notexecuted", "0"))
        else:
            #todo handle missing statistic
            print("missing statistic in summary")
            return junit_element

        junit_testsuite = testsuite(
            name=module_name,
            uuid=module_uuid,
            errors=notok,
            failures=0,
            skipped=notexecuted,
            tests=total,
            time=0.0,
            timestamp=f"{date}T{time}",
            hostname=host,
         )

        junit_element.add_testsuite(junit_testsuite)

        all_testobject = tessy_element.findall("testobject")

        for testobject in all_testobject:
            all_testcases = testobject.findall("testcase")
            for testcase_element in all_testcases:
                junit_testsuite.add_child(tessy2junit_testcase(testcase_element))

        return junit_element
    else:
        print("missing report in xml file")
        return junit_element



def tessy2junit(text: str) -> str:
    # translate text to xml structure
    tessy_root = ET.fromstring(text)

    # create junit root
    junit_root = testsuites(name="tessy tests")

    junit_root = tessy2junit_testsuite(tessy_root, junit_root)

    junit_root_xml = junit_root.to_element()

    # xml structure to string
    return ET.tostring(junit_root_xml, encoding="utf-8").decode("utf-8")

def parse_folder(input_folder: Path, output_folder: Path) -> None:
    """
    P

    :param input_folder: Path to the folder containing files to be anonymized.
    :param output_folder: Path to the folder where anonymized files will be saved.
    """
    if not input_folder.is_dir():
        print(f"Error: The input folder '{input_folder}' does not exist or is not a directory.")
        return

    for file_path in input_folder.glob("*.xml"):
        print(f"Parsing file: {file_path.absolute()}")
        #try:
        if True:
            with file_path.absolute().open("r", ) as f_in:
                text = f_in.read()

            junit_xml_str = tessy2junit(text)

            output_file_path = output_folder / file_path.name
            output_file_path.write_text(junit_xml_str)
            print(f"Anonymized file saved to: {output_file_path}")
        #except Exception as e:
        #    print(f"Error processing file '{file_path}': {e}")

def main():
      import argparse

      parser = argparse.ArgumentParser(description=".")
      parser.add_argument("-i", "--input_folder", help="Path to the input folder containing XML files.", required=True, type=Path)
      parser.add_argument("-o", "--output_folder", help="Path to the output folder for anonymized XML files.", required=True, type=Path)

      args = parser.parse_args()

      parse_folder(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
