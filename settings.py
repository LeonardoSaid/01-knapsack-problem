EVALUATE_METHODS_SETTINGS = {
    'ssl': {
        'enable': False
    },
    'msl': {
        'enable': False,
        'max_iterations': 100
    },
    'ils': {
        'enable': False,
        'max_iterations': 100
    },
    'vns': {
        'enable': True,
        'max_iterations': 100,
        'neighborhood_size': 2
    },
    'tabu': {
        'enable': True,
        'max_iterations': 100,
        'tenure': 7
    },
    'sa': {
        'enable': True,
        'max_iterations': 100,
        'initial_temperature': 300,
        'distance': 2
    }
}

# parameters used for low comparison

# EVALUATE_METHODS_SETTINGS = {
#     'ssl': {
#         'enable': False
#     },
#     'msl': {
#         'enable': False,
#         'max_iterations': 500
#     },
#     'ils': {
#         'enable': False,
#         'max_iterations': 500
#     },
#     'vns': {
#         'enable': False,
#         'max_iterations': 500,
#         'neighborhood_size': 2
#     },
#     'tabu': {
#         'enable': True,
#         'max_iterations': 500,
#         'tenure': 7
#     },
#     'sa': {
#         'enable': False,
#         'max_iterations': 500,
#         'initial_temperature': 300,
#         'distance': 2
#     }
# }
