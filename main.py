import PySimpleGUI as sg
from client import Client

if __name__ == '__main__':
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Server IP'), sg.Input(default_text="localhost" ,key='-IP-')],
        [sg.Text('Port'), sg.Input(default_text=9999, key='-PORT-')],
        [sg.Text('Your Name'), sg.Input('test', key='-NAME-')],
        [sg.Button('Connect')]
    ]
    window = sg.Window('Chat App - Connect to Server', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == 'Connect':
            ip = values['-IP-']
            port = int(values['-PORT-'])
            name = values['-NAME-']
            window.hide()
            Client(ip, port, name)
            break

    window.close()