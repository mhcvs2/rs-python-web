from validator import *


add_rules = {
    'region_code': [
        Required, InstanceOf(basestring), Not(Blank())
    ],
    'product_type_id': [
        Required, InstanceOf(int)
    ],
    'gp_name': [
        Required, InstanceOf(basestring), Pattern('^[a-zA-Z0-9_?-?]*$')
    ],
    'item_no': [
        Required, In(["CU", "DCU"])
    ],
    'value_dev': [
        Required, InstanceOf(int)
    ],
    'value_prod': [
        Required, InstanceOf(int)
    ]
}
