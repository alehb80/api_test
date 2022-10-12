from backend.config.globals import odm

if __name__ == '__main__':
    my_dict = {
        "key":     2,
        "payload": "test"
    }
    odm.save(my_dict)
