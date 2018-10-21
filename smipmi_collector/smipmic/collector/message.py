import re

from smipmic.util.message import Message

class PminfoMessage(Message):
    """
    Takes raw `pminfo` measurement text data as input
    Takes care of parsing the different components
    Outputs parsed measurement data (temp, fanspeed, wattage) for a module (i.e. PSU)
    """
    RE_MODULE = re.compile('\s\[[a-zA-Z]+\s=\s(.+)\]\s\[[a-zA-Z]+ (?P<instance>\d)\]')
    RE_FIELDS = re.compile(r'^\s(?P<key>(?:\S|\s(?!\s))+)\s+\|\s+(?P<val>.+)$')
    MSG_KEYWORDS = ['Temperature', 'Main Output Power', 'Input Power', 'Fan']
    PREAMBLE_LEN = 3

    @classmethod
    def _test(cls, data: str):
        re_match = cls.RE_MODULE.search(data)
        kw_match = all([kw in data for kw in cls.MSG_KEYWORDS])
        return re_match and kw_match

    def get_module(self):
        module = self.RE_MODULE.search(self._data)
        if module:
            return module.groupdict().get('instance')
        raise MessageHasUnknownInstanceError('PSU instance could not be determined.')
