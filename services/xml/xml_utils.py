from lxml import etree
import re


def xml_parse(xml_data):
    if etree.iselement(xml_data):
        return xml_data
    else:
        # Remove the default namespace definition (xmlns="http://some/namespace")
        xml_data = re.sub(r'\sxmlns="[^"]+"', '', xml_data, count=1)
        parsed_xml = etree.fromstring(xml_data)
        return parsed_xml


def redaction_elements(xml_data, remove_xpaths):
    xml = xml_parse(xml_data)
    for xpath in remove_xpaths:
        element = xml.xpath(xpath)
        if element:
            e = element[0]
            e.getparent().remove(e)
    return xml


def chronological_redactable_elements(elements):
    return sorted(elements, key=lambda x: x.parsed_date(), reverse=True)


def alphabetical_redactable_elements(elements):
    return sorted(elements, key=lambda x: x.description().lower(), reverse=False)


def normalize_data(context_data):
    """
    fill all empty places
    """
    max_elements_count = 7
    for data in context_data:
        if len(context_data[data]) > max_elements_count:
            max_elements_count = len(context_data[data])
    for data in context_data:
        if len(context_data[data]) < max_elements_count:
            length = max_elements_count - len(context_data[data])
            while length:
                context_data[data].append([])
                length = length - 1
    return context_data
