# coding: UTF-8

from classes.log import Log as Log
import math
import random


class GeneratePassword:

    def __init__(self, length):
        self.length = length
        self.log = Log()

    def generate(self):
        i = 0

        # パスワード生成に使用する文字列
        num = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        letter = (
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        )
        capital = (
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        )
        mark = ("@", "%", ":", "!", "-", "_")

        # パスワード桁数をint型に変換
        length = self.length

        if length < 1:
            self.log.write("error", "エラー：パスワード桁数＜1")
            return False

        password = ""

        while i < length:
            i += 1

            # 文字列をランダム生成
            param = math.ceil(random.random() * 4)
            if param == 1:
                password += num[math.floor(random.random() * len(num))]

            elif param == 2:
                password += letter[math.floor(random.random() * len(letter))]

            elif param == 3:
                password += capital[math.floor(random.random() * len(capital))]

            elif param == 4:
                password += mark[math.floor(random.random() * len(mark))]

        return password

    def generateWithoutSymbol(self):
        i = 0

        # パスワード生成に使用する文字列
        num = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        letter = (
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        )
        capital = (
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        )

        # パスワード桁数をint型に変換
        length = self.length

        if length < 1:
            self.log.write("error", "エラー：パスワード桁数＜1")
            return False

        password = ""

        while i < length:
            i += 1

            # 文字列をランダム生成
            param = math.ceil(random.random() * 3)
            if param == 1:
                password += num[math.floor(random.random() * len(num))]

            elif param == 2:
                password += letter[math.floor(random.random() * len(letter))]

            elif param == 3:
                password += capital[math.floor(random.random() * len(capital))]

        return password
