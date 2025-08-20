from GUI.GUI_bot import Interface_bot

import tkinter as tk


def main():

    ventana = tk.Tk()

    GUI_bot = Interface_bot()
    GUI_bot.generar_ventana(ventana)

    # Ejecutar la aplicación
    ventana.mainloop()


if __name__ == "__main__":
    main()
