def get_obj_from_callback(field):
    try:
        return field.split('_', 2)[1]
    except IndexError:
        return field
