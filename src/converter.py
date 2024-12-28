# coding: UTF-8

import PySimpleGUI as sg
from classes.encryption import Encryption as Encryption

# ウィジェットのプロパティ
font = ("meiryo", 20)
size = (20, 3)

layout = [
    [sg.Text("文字列暗号化・復号化", size=(20,2), font=font)],
    [sg.Text("暗号化文字列", font=font), sg.InputText(size=size, font=font, key="t_encrypt")],
    [sg.Text("復号化文字列", font=font), sg.InputText(size=size, font=font, key="t_decrypt")],
    [sg.Button("暗号化", font=font, key="encrypt"), sg.Button("復号化", font=font, key="decrypt"), 
     sg.Button("アプリ終了", font=font, key="cancel")]
]

window = sg.Window("文字列暗号化・復号化", layout)

while True:
    event, value = window.read()
    encryption = Encryption()

    enc_word = value["t_encrypt"]
    dec_word = value["t_decrypt"]

    if event == None:
        break

    if event == "encrypt":
        # 暗号化
        if dec_word != '':
            window['t_encrypt'].update(encryption.encrypt(dec_word))

    if event == "decrypt":
        # 復号化
        if enc_word != '':
            window['t_decrypt'].update(encryption.decrypt(enc_word))
    
    if event == "cancel":
        break

window.close()