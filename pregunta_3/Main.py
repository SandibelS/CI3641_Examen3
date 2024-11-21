import Classes

def main():
        
    seguir_ejecutandose : bool = True
    simulador : Classes.Simulador = Classes.Simulador()

    while seguir_ejecutandose:

        input_usuario_str : str = input()

        if input_usuario_str == "":
            print("Se necesita una accion")
            continue

        input_usuario_list : list[str] = input_usuario_str.split(" ")

        if input_usuario_list[0] == "ATOMICO":
            
            if len(input_usuario_list) < 4:
                print("Insuficientes argumentos")
                continue
            if len(input_usuario_list) > 4:
                print("Demasiados argumentos")
                continue

            nombre = input_usuario_list[1]
            representacion = input_usuario_list[2]
            alineacion = input_usuario_list[3]

            try:
                simulador.definir_atomico(nombre, int(representacion), int(alineacion))
            except Exception as e:
                print(f"Error: {e}")

        elif input_usuario_list[0] == "STRUCT":
            if len(input_usuario_list) == 1:
                print("Insuficientes argumentos")
                continue

            nombre = input_usuario_list[1]
            lista_tipos = input_usuario_list[2:]

            try:
                simulador.definir_struct(nombre, lista_tipos)
            except Exception as e:
                print(f"Error: {e}")

        elif input_usuario_list[0] == "UNION":
            if len(input_usuario_list) == 1:
                print("Insuficientes argumentos")
                continue

            nombre = input_usuario_list[1]
            lista_tipos = input_usuario_list[2:]

            try:
                simulador.definir_union(nombre, lista_tipos)
            except Exception as e:
                print(f"Error: {e}")

        elif input_usuario_list[0] == "DESCRIBIR":

            if len(input_usuario_list) < 2:
                print("Insuficientes argumentos")
                continue
            if len(input_usuario_list) > 2:
                print("Demasiados argumentos")
                continue

            nombre = input_usuario_list[1]

            s = f'Descripcion del tipo "{nombre}":  \n'
            try:
                d : Classes.Descripcion = simulador.describir_sin_empaquetacion(nombre)
                s += "\t Si el lenguaje guarda registros y registros viariantes sin empaquetar.\n"
                s += f"\t\t Tamaño: {d.tam} bytes \n"
                s += f"\t\t Alineacion: {d.alineacion} \n"
                s += f"\t\t Cantidad de bytes desperdiciados: {d.cant_bytes_desperdiciados} bytes \n"

                d = simulador.describir_con_empaquetacion(nombre)
                s += "\t Si el lenguaje guarda registros y registros viariantes empaquetados.\n"
                s += f"\t\t Tamaño: {d.tam} bytes \n"
                s += f"\t\t Alineacion: {d.alineacion} \n"
                s += f"\t\t Cantidad de bytes desperdiciados: {d.cant_bytes_desperdiciados} bytes \n"
          
                d = simulador.describir_con_reorganizacion(nombre)
                s += "\t El lenguaje guarda registros y registros viariantes reordenando los campos de manera óptima.\n"
                s += f"\t\t Tamaño: {d.tam} bytes \n"
                s += f"\t\t Alineacion: {d.alineacion} \n"
                s += f"\t\t Cantidad de bytes desperdiciados: {d.cant_bytes_desperdiciados} bytes"

            except Exception as e:
                print(f"Error: {e}")

            print(s)

        elif input_usuario_list[0] == "SALIR":
        
            seguir_ejecutandose = False

        else:
            print("Accion no reconocida")

