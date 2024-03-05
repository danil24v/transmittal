from collections import namedtuple

REGEXP_APAR = '^(PH|PI)\d{5}$'
REGEXP_SYSMOD = '^(PH|PI|UI|UJ)\d{5}$'
REGEXP_TICKET = '^[a-zA-Z]{3,8}-\d{3,6}$'
REGEXP_FMID = '^[A-Z0-9$@]{6,8}$'
REGEXP_MODNAMES = '^(,{0,1}[A-Z0-9$@]{3,8}){1,100}$'
REGEXP_CUST = '^[A-Z0-9$@,;*&+)(]{1,100}$'
REGEXP_CLCODE = '^[A-Z0-9$]{2,10}$'
REGEXP_RKT_COMPONENT = '^[)(a-zA-Z0-9\s]{3,18}(,[)(a-zA-Z0-9\s]{3,18}){0,4}$'
REGEXP_RKT_TYPE = '^[a-zA-Z0-9]{3,10}$'
REGEXP_MULTI_DESC = '^(\n{0,1}[a-zA-Z0-9]{0,50}){0,10}$'    # first {} - line len, second {} - lines count

LEGAL_CHECKLIST = [
    {'id': 'q1', "must": False, 'text': '1. Does this fix contain any code licensed from a third party (other than open source)?', 'parent': ''},
    {'id': 'q1a', "must": False, 'text': '1A. Do you have legal approval for shipping this version of the third party code in the maintenance stream?', 'parent': 'q1'},
    {'id': 'q1b', "must": False, 'text': '1B. Does the shipping of the third party code require entitlement?', 'parent': 'q1'},
    {'id': 'q2', "must": False, 'text': '2. Does this fix contain any open source?', 'parent': ''},
    {'id': 'q2a', "must": False, 'text': '2A. Do you have OSSC approval for shipping this version of the open source in the maintenance stream?', 'parent': 'q2'},
    {'id': 'q2b', "must": False, 'text': '2B. Is the open source being distributed in accordance with any restrictions imposed by legal or the OSSC?', 'parent': 'q2'},
    {'id': 'q2c', "must": False, 'text': '2C. Does the shipping of the open source require entitlement?', 'parent': 'q2'},
    {'id': 'q3', "must": False, 'text': '3. Does this fix contain any license or master keys?', 'parent': ''},
    {'id': 'q3a', "must": False, 'text': '3A. Has legal approved shipping the keys?', 'parent': 'q3'},
    {'id': 'q3b', "must": False, 'text': '3B. Does the shipping of the license or master keys require entitlement?', 'parent': 'q3'},
    {'id': 'q4', "must": False, 'text': '4. Does this fix, or this fix in combination with other fixes, enable functionality that only entitled customers should have? For example, full product included.', 'parent': ''},
    {'id': 'q5', "must": False, 'text': '5. Is this fix subject to any export restrictions due to its content, such as encryption, sensitive content or because of any other export requirements?', 'parent': ''},
    {'id': 'q6', "must": True, 'text': '6. If removing documented function/APIs in this fix, have you received approval through your organizations official approval process? (Answer yes if you are not removing documented function/APIs)', 'parent': ''},
    {'id': 'q7', "must": False, 'text': '7. Does the fix or any customer visible documentation about the fix, contain any IBM or client sensitive information (i.e., username, password or personally identifiable information)?', 'parent': ''}
]

ClosingField = namedtuple("ClosingCode", ["name", "regexp", "linelen", "maxsize", "is_urgent"])
CLOSING_CODES = {
    "PER": [
        ClosingField("Problem Conclusion",  "^[a-zA-Z0-9]*$", 10, 100, True),
        ClosingField("Problem Decription",  "^[a-zA-Z0-9]*$", 10, 100, True)
    ],
    "UR1": [
        ClosingField("Something", "^[a-zA-Z0-9]*$", 10, 100, True),
        ClosingField("Comments", "^[a-zA-Z0-9]*$", 10, 100, False)
    ]
}

HoldField = namedtuple("HoldField", ["regexp", "linelen", "maxsize", "allowfew"])
HOLD_FIELDS = {
    "IBM": {
        "ACTION": HoldField("^[a-zA-Z0-9\\\\s!#@$]*$", 80, 9999, False),
        "DB2BIND": HoldField("^[a-zA-Z0-9\\\\s!#@$]*$", 80, 9999, True)
    },
    "ROCKET": {
        "ACTION": HoldField("^[a-zA-Z0-9\\\\s!#@$]*$", 80, 9999, False),
        "DB2BIND": HoldField("^[a-zA-Z0-9\\\\s!#@$]*$", 80, 9999, True)
    }
}

 