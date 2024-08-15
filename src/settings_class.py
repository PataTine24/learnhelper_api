"""
This class is adding the option to save config data locally onthe client and read it in before
the app starts. With this we have access to
        "person_data": {"id", "name" , "password"},
        "visual_data": {"theme" , "resolution" },
        resolution = tuple[x,y]
        "db_data": {"host" , "user" , "password" , "database" }
"""
# TODO: Better documentation here
import json
from os import path
import traceback


class InvalidSettingsKey(Exception):
    def __init__(self, message: str = None, error_code=None, searched_key: str = ""):
        if message is None:
            message = f"The settings key you searched for({searched_key}) is not existing"
        else:
            self.message = message
        super().__init__(message)
        self.error_code = error_code
        self.traceback = ''.join(traceback.format_stack())


class SettingsManager:
    """
    Has access to
        "person_data": {"id", "name" , "password"},
        "visual_data": {"theme" , "resolution" },
        size = tuple(x,y)
        "db_data": {"host" , "user" , "password" , "database" }
    """

    def __init__(self, filepath='../settings.json'):
        self.__filepath = filepath
        self.__settings = {
            "person_data": {"id": 0, "name": "empty", "password": "<PASSWORD>"},
            "visual_data": {"theme": "litera", "resolution": (800, 600)},
            "db_data": {"host": "localhost", "user": "root", "password": "12345", "database": "learnhelper"}
        }

    def import_settings(self):
        """
        imports settings from the json file declared in the object.
        standard is source folder -> up as settings.json
        """
        if path.exists(self.__filepath):
            with open(self.__filepath, 'r') as file:
                content = file.read().strip()
                if content == "":
                    print(f"Error: The file {self.__filepath} is empty. Loading default settings.")
                else:
                    try:
                        self.__settings = json.loads(content)
                    except json.JSONDecodeError:
                        print(f"Error: The file {self.__filepath} contains invalid JSON. Loading default settings.")
        else:
            print(f"Error: The file {self.__filepath} does not exist. Loading default settings.")

    def export_settings(self):
        """
        exports settings to the json file declared in the object.
        standard is source folder -> up as settings.json
        """
        with open(self.__filepath, 'w') as json_file:
            # dump with extra params makes it better readable
            json.dump(self.__settings, json_file, indent=4, sort_keys=True)

    def get_settings(self, *args) -> dict:
        """
        Gets local setting from the own attribute. Its a dict.
        You get returned the setting key based on the number of args.
        1 arg above setting like "person_data"
        2 args directly the value of a specific setting.
        """
        if len(args) == 1:
            if args[0] in self.__settings:
                return self.__settings.get(args[0], {})
            else:
                raise InvalidSettingsKey(searched_key=args[0])
        elif len(args) == 2:
            if args[0] in self.__settings:
                if args[1] in self.__settings[args[0]]:
                    return self.__settings.get(args[0], {}).get(args[1], {})
                else:
                    raise InvalidSettingsKey(searched_key=f"{args[0]}[\"{args[1]}\"]")
            else:
                raise InvalidSettingsKey(searched_key=args[0])
        elif len(args) >= 3:
            raise InvalidSettingsKey(message=f"Settings only have main and subkey. You gave {len(args)} args!")
        else:
            return self.__settings

    def set_settings_key(self, mainkey: str, subkey: str, value):
        if mainkey in self.__settings and subkey in self.__settings[mainkey]:
            self.__settings[mainkey][subkey] = value
            self.export_settings()
        else:
            raise InvalidSettingsKey(searched_key=f"{mainkey}:{subkey}")

if __name__ == "__main__":
    print("This module is not working alone")



