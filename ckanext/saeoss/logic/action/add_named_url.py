import uuid
import re
import ckan.plugins.toolkit as tk


def populate_dataset_name(data_dict: dict, context: dict, calls:int = 0):
    """Adding uuid to the named url
    , the name field was a bit
    confusing to the client.
    """
    title = data_dict.get("title")
    if data_dict.get('name'):
        name = _remove_special_characters_from_package_url(data_dict.get('name'))
    else:
        name = _remove_special_characters_from_package_url(title)
    
    validation_dict = {"name":name}
    schema = {"name": [tk.get_validator("package_name_exists")]}
    data,error = tk.navl_validate(validation_dict,schema, context)
    if error:
        return name

    calls += 1
    if re.search(r'-\d$',name):
        name = re.sub(r'-\d$', '', name)
        name = name+'-'+str(calls)
    else:
        name = name+'-'+str(calls)
    data_dict['name'] = name
    return populate_dataset_name(data_dict, context, calls)


def _remove_special_characters_from_package_url(url):
    """Special characters are not
    accepted by CKAN for dataset
    urls, replace them
    """
    special_chars = "!\"”'#$%&'()*+,-./:;<=>?@[\]^`{|}~.[] "
    if url is not None:
        for i in url:
            if i in special_chars:
                url = url.replace(i, "-")

        return url
