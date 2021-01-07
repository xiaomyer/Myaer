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
        self.guilds = DataEntry("data/guilds.json", "guild_id", GuildConfig)
        self.users = DataEntry("data/users.json", "user_id", UserConfig)


class DataEntry:
    def __init__(self, data, id_string, construct):
        self.data = TinyDB(data)
        self.id_string = id_string
        self.construct = construct
        self.cache = {}

    def get(self, id_):
        if config := self.cache.get(id_): return config
        data = self.data.search(where(self.id_string) == id_)
        if data: config = self.construct(data[0])
        self.cache[id_] = config
        return config if data else None

    def set(self, id_, key, value):
        result = self.data.search(where(self.id_string) == id_)
        if result:
            self.data.update({key: value}, where(self.id_string) == id_)
            if self.cache.get(id_):
                self.cache.pop(id_)
        else:
            self.data.insert({self.id_string: id_, key: value})

    def delete(self, id_, key):
        result = self.data.search(where(self.id_string) == id_)
        if not result:
            return
        saved = result[0].get(key)
        if saved:
            self.data.update(delete(key), where(self.id_string) == id_)
            if self.cache.get(id_):
                self.cache.pop(id_)
            return saved  # return what was deleted
        else:
            return
