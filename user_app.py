import os, re, sys, termios

DEV_PATH = "/dev/-----"  #nombre de mi archivo

def main():
    i = 0
    #i--> MENU SETCONFIG GETCONFIG START STOP
    msg = ""
    while True:
        match i:
            #main menu
            case 0:
                match main_menu():
                    case "1":
                        #GOTO env_config
                        menu = 1
                    case "2":
                        #GOTO env_peek
                        menu = 2
                    case "3":
                        #GOTO Start
                        menu = 3
                    case "4":
                        #GOTO Stop
                        menu = 4
                    case "5":
                        print("*****************************************")
                        print("Seguro?:")
                        print("*****************************************")
                        print("1--> Si")
                        print("2--> No")
                        print("*****************************************")
                        print("")
                        match input("[1-2]: ").strip():
                            case "1":
                                os.system("clear")
                                break
                    case _:
                        print("\nOpción invalida")
                        flush_stdin()
                        input("Presione tecla para continuar...")
            #Enviar Config
            case 1:
                temp = env_config()
                match temp:
                    case "1": msg = "Sp"
                    case "2": msg = "ErrSp"
                    case "3": msg = "Mode"
                    case "4": i=0
                    case _:
                        print("\nOpción invalida")
                        flush_stdin()
                        input("Presione tecla para continuar...")
                
                if temp in ["1","2","3"]:
                    match temp:
                        case "1":
                            print("")
                            print("*****************************************")
                            print("")
                            print("Ingrese Setpoint [0-360]: ")
                            flush_stdin()
                            

    a=0

def main_menu():
    os.system("clear") #envio comando clear
    print("*****************************************")
    print("*********{ User Space UART EGB }*********")
    print("*****************************************")
    print(" ")
    print("Ingrese acción:")
    print(" ")
    print("1--> Enviar configuración")
    print("2--> Recibir información")
    print("3--> Iniciar funcionamiento")
    print("4--> Terminar funcionamiento")
    print("5--> Terminar ejecución")
    print(" ")
    flush_stdin()
    return input("[1-5] :").strip()

def env_config():
    print("*****************************************")
    print("***{ Seleccione variable a configurar }***")
    print("*****************************************")
    print("1--> Setpoint")
    print("2--> Error de Setpoint")
    print("3--> Elegir Modo")
    print("4--> Regresar al menu anterior")
    print("*****************************************")
    print("")
    #flush_stdin()
    return input("[1-4] :").strip()


def flush_stdin():
    termios.tcflush(sys.stdin, termios.TCIFLUSH)

if __name__ == "__main__" :
    main()