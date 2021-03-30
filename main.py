from commands import COMMANDS


# Обработчик консольных команд
def start():
    print('Введите \'help\' для справки')
    str = input('$>')

    # Цикл для консольных команд
    while str.split(' ')[0] != 'exit':
        cmnd = str.split(' ')[0]
        params = str.split(' ')[1:]

        if cmnd in COMMANDS.keys():
            f = COMMANDS[cmnd]
            try:
                f(params)
            except Exception as e:
                print(e)
        else:
            print('Команды {} не существует, введите \'help\' для справки'.format(cmnd))

        str = input('\n$>')


if __name__ == '__main__':
    start()
