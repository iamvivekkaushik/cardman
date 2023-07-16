# This function is used to validate the filter data and return a dictionary with only valid keys
def validate_filter(model, dictionary, allowed_keys=None):
    if allowed_keys is None:
        allowed_keys = []
    model_keys = [field.name for field in model._meta.fields]

    # remove the fields that are not allowed
    for key in allowed_keys:
        if key not in model_keys:
            model_keys.remove(key)

    # add gte and lte to the list of keys and create a new list
    key_list = model_keys.copy()
    key_list += [key + "__gte" for key in model_keys]
    key_list += [key + "__lte" for key in model_keys]

    final_data = {}

    for key in dictionary.keys():
        if key in key_list:
            final_data[key] = dictionary[key]

    return final_data
