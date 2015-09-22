from tweepy.parsers import Parser


class RawJsonParser(Parser):

    def parse(self, method, payload):
        return payload