"""
MIT License

Copyright (c) 2020 myerfire

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .objects import UserConfig, GuildConfig
from tinydb import TinyDB, where
from tinydb.operations import delete


class Data:
    def __init__(self):
        print("------------------------------")
        self.guilds = DataEntry("data/guilds.json", "guild_id", GuildConfig)
        print("Initialized guild configurations")
        self.users = DataEntry("data/users.json", "user_id", UserConfig)
        print("Initialized user configurations")


class DataEntry:
    def __init__(self, data, id_string, construct):
        self.data = TinyDB(data)
        self.id_string = id_string
        self.construct = construct
        self.cache = {}

    def get(self, id_):
        print("------------------------------")
        print(f"Attempting configuration get for object {self.id_string}\n"
              f"ID: {id_}")
        if config := self.cache.get(id_):
            print(f"Returning configuration from cache")
            return config
        data = self.data.search(where(self.id_string) == id_)
        if data: config = self.construct(data[0])
        self.cache[id_] = config
        print(f"Saved configuration to cache")
        print("Successfully got configuration" if data else
              "Failed to get configuration\n"
              "Configuration does not exist\n"
              "Returned default configuration")
        return config if data else self.construct.default()

    def get_silent(self, id_):  # same as above but no logging because this is called every message and way too spammy
        if config := self.cache.get(id_):
            return config
        data = self.data.search(where(self.id_string) == id_)
        if data: config = self.construct(data[0])
        self.cache[id_] = config
        return config if data else self.construct.default()

    def set(self, id_, key, value):
        print("------------------------------")
        print(f"Attempting configuration set for object {self.id_string}\n"
              f"ID: {id_}\n"
              f"Key: {key}\n"
              f"Value: {value}")
        result = self.data.search(where(self.id_string) == id_)
        if result:
            self.data.update({key: value}, where(self.id_string) == id_)
            print("Updated configuration")
            if self.cache.get(id_):
                self.cache.pop(id_)
                print(f"Removed configuration from cache")
        else:
            self.data.insert({self.id_string: id_, key: value})
            if self.cache.get(id_):
                self.cache.pop(id_)
                print(f"Removed configuration from cache")
            print("Created configuration")
            print("Updated configuration")

    def delete(self, id_, key):
        print("------------------------------")
        print(f"Attempting configuration key delete for object {self.id_string}\n"
              f"ID: {id_}\n"
              f"Key: {key}")
        result = self.data.search(where(self.id_string) == id_)
        if not result:
            print("Failed to delete key in configuration\n"
                  "Configuration does not exist")
            return
        saved = result[0].get(key)
        if saved:
            self.data.update(delete(key), where(self.id_string) == id_)
            print("Deleted key of configuration for object")
            if self.cache.get(id_):
                self.cache.pop(id_)
                print(f"Removed configuration from cache")
            return saved  # return what was deleted
        else:
            print("Failed to delete key in configuration\n"
                  "Key in configuration does not exist")
            return
