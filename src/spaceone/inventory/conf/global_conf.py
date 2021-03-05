CONNECTORS = {
}

LOG = {
    'filters': {
        'masking': {
            'rules': {
                'Collector.collect': [
                    'secret_data'
                ],
                'Collector.verify': [
                    'secret_data'
                ],
            }
        }
    }
}

HANDLERS = {
}

ENDPOINTS = {
}
