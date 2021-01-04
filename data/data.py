"""
MIT License

Copyright (c) 2020 MyerFire

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
from tinydb import TinyDB, Query, where
from tinydb.operations import delete


class Data:
    def __init__(self):
        self.guilds = Guilds()
        self.users = Users()


class Guilds:
    def __init__(self):
        self.data = TinyDB("data/guilds.json")
        self.cache = {}

    def get(self, id_):
        if config := self.cache.get(id_): return config
        data = self.data.search(where("guild_id") == id_)
        if data: config = GuildConfig(data[0])
        self.cache[id_] = config
        return GuildConfig(data[0]) if data else None

    def set(self, id_, key, value):
        result = self.data.search(where("guild_id") == id_)
        if result:
            self.data.update({key: value}, where("guild_id") == id_)
        else:
            self.data.insert({"guild_id": id_, key: value})
        self.cache.pop(id_)

    def delete(self, id_, key):
        query = Query()
        result = self.data.search(where("guild_id") == id_)
        if not result:
            return
        saved = result[0].get(key)
        if saved:
            self.data.update(delete(key), query.guild_id == id_)
            self.cache.pop(id_)
            return saved  # return what was deleted
        else:
            return


class Users:
    def __init__(self):
        self.data = TinyDB("data/users.json")
        self.cache = {}

    def get(self, id_):
        if config := self.cache.get(id_): return config
        data = self.data.search(where("user_id") == id_)
        if data: config = UserConfig(data[0])
        self.cache[id_] = config
        return UserConfig(data[0]) if data else None

    def set(self, id_, key, value):
        result = self.data.search(where("user_id") == id_)
        if result:
            self.data.update({key: value}, where("user_id") == id_)
        else:
            self.data.insert({"user_id": id_, key: value})
        self.cache.pop(id_)

    def delete(self, id_, key):
        query = Query()
        result = self.data.search(where("user_id") == id_)
        if not result:
            return
        saved = result[0].get(key)
        if saved:
            self.data.update(delete(key), query.user_id == id_)
            self.cache.pop(id_)
            return saved  # return what was deleted
        else:
            return
