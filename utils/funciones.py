import os
from utils.menus import *
from utils.jsonFileHandler import *
from datetime import datetime
import time


# Ruta del archivo de datos (persistencia en JSON)
DATA_FILE = "./data/datadata.json"


def limpiar():
    # Limpia la consola según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    # Pausa la ejecución hasta que el usuario presione Enter
    try:
        input("Presione Enter para continuar...")
    except KeyboardInterrupt:
        # Maneja Ctrl+C para que no cierre bruscamente
        print('No pasaras 🧙')


def imprimirMenus(title, options):
    # Imprime un menú genérico con título y una lista de opciones
    choise = 0
    index = 1
    limpiar()
    print("━" * 50)
    print(f"━━ {title:^44} ━━")
    print("━" * 50)
    print("━━")
    for item in options:
        print(f"{index}. {item}")
        index += 1
    
    # Bucle para validar la opción ingresada por el usuario
    while True:
        try:
            try:
                choise = int(input('--> '))
            except KeyboardInterrupt:
                print('No pasaras 🧙')
            if choise not in range(1, len(options) + 1):
                print("--> Opción inválida...")
            else:
                break
        except ValueError:
            print("Su elección debe ser un número...")
    return choise


def validarInput(mensaje='--> ', tipo='int'):
    # Envuelve input con conversión de tipo y manejo de errores
    while True:
        try:
            valor = input(mensaje)
            if tipo == 'int':
                return int(valor)
            elif tipo == 'float':
                return float(valor)
            else:
                # Cualquier otro tipo se maneja como string
                return valor
        except ValueError:
            print(f"Debe ingresar un valor válido ({tipo})...")
        except KeyboardInterrupt:
            print("\nNo se permiten interrupciones.")


def inicializarDatos():
    """Inicializa la estructura de datos si no existe"""
    # Estructura base del sistema: pizzas, adicionales y facturas
    estructura_inicial = {
        "pizzas": {
            "1": {"nombre": "Margarita", "precio": 12.50, "activa": True},
            "2": {"nombre": "Pepperoni", "precio": 14.00, "activa": True},
            "3": {"nombre": "Hawaiana", "precio": 13.50, "activa": True},
            "4": {"nombre": "Cuatro Quesos", "precio": 15.00, "activa": True}
        },
        "adicionales": {
            "1": {"nombre": "Queso Extra", "precio": 2.00, "activo": True},
            "2": {"nombre": "Champiñones", "precio": 1.50, "activo": True},
            "3": {"nombre": "Aceitunas", "precio": 1.00, "activo": True}
        },
        "facturas": []
    }
    # Crea el archivo JSON si no existe con esta estructura
    initialize_json(DATA_FILE, estructura_inicial)


def generarIdFactura():
    """Genera un ID único para la factura"""
    # Lee todas las facturas y calcula el siguiente ID incremental
    datos = read_json(DATA_FILE)
    facturas = datos.get("facturas", [])
    if not facturas:
        return 1
    return max([f["id"] for f in facturas]) + 1


def tomarOrden():
    """Permite al mesero tomar una orden"""
    limpiar()
    print("━" * 50)
    print("━━" + "TOMAR ORDEN".center(46) + "━━")
    print("━" * 50)
    
    # Carga datos actuales desde el JSON
    datos = read_json(DATA_FILE)
    # Filtra solo pizzas activas
    pizzas = {k: v for k, v in datos["pizzas"].items() if v["activa"]}
    # Filtra solo adicionales activos
    adicionales = {k: v for k, v in datos["adicionales"].items() if v["activo"]}
    
    if not pizzas:
        # Si no hay pizzas activas, no se puede tomar orden
        print("\nNo hay pizzas disponibles en este momento.")
        pausar()
        return
    
    # Mostrar pizzas disponibles
    print("\nPIZZAS DISPONIBLES:")
    for id_pizza, pizza in pizzas.items():
        print(f"  {id_pizza}. {pizza['nombre']} - ${pizza['precio']:.2f}")
    
    # Lista donde se acumulan los items elegidos en la orden
    items_orden = []
    while True:
        try:
            try:
                # Permite ingresar múltiples pizzas hasta escribir 'fin'
                id_pizza = input("\nID de pizza (o 'fin' para terminar): ")
            except KeyboardInterrupt:
                print('No pasaras 🧙')
            if id_pizza.lower() == 'fin':
                break
            
            if id_pizza not in pizzas:
                print("Pizza no válida. Intente de nuevo.")
                continue
            
            cantidad = validarInput("Cantidad: ", 'int')
            if cantidad <= 0:
                print("La cantidad debe ser mayor a 0.")
                continue
            
            # Agrega el item pizza a la orden
            items_orden.append({
                "tipo": "pizza",
                "id": id_pizza,
                "nombre": pizzas[id_pizza]["nombre"],
                "precio": pizzas[id_pizza]["precio"],
                "cantidad": cantidad
            })
            print(f"{cantidad}x {pizzas[id_pizza]['nombre']} agregada(s)")
        except KeyboardInterrupt:
            # Si interrumpe en medio de la toma de orden, se cancela
            print("\nOperación cancelada.")
            return
    
    if not items_orden:
        # No se registró nada en la orden
        print("\nNo se agregaron items a la orden.")
        pausar()
        return
    
    # Agregar adicionales
    if adicionales:
        print("\nADICIONALES DISPONIBLES:")
        for id_adic, adic in adicionales.items():
            print(f"  {id_adic}. {adic['nombre']} - ${adic['precio']:.2f}")
        
        agregar_adic = input("\n¿Desea agregar adicionales? (s/n): ").lower()
        if agregar_adic == 's':
            while True:
                try:
                    # Permite agregar múltiples adicionales hasta 'fin'
                    id_adic = input("ID de adicional (o 'fin' para terminar): ")
                except KeyboardInterrupt:
                    print('No pasaras 🧙')
                if id_adic.lower() == 'fin':
                    break
                
                if id_adic not in adicionales:
                    print("Adicional no válido.")
                    continue
                
                cantidad = validarInput("Cantidad: ", 'int')
                if cantidad <= 0:
                    print("La cantidad debe ser mayor a 0.")
                    continue
                
                # Agrega el adicional como otro item de la orden
                items_orden.append({
                    "tipo": "adicional",
                    "id": id_adic,
                    "nombre": adicionales[id_adic]["nombre"],
                    "precio": adicionales[id_adic]["precio"],
                    "cantidad": cantidad
                })
                print(f"{cantidad}x {adicionales[id_adic]['nombre']} agregado(s)")
    
    # Calcular total de la orden sumando precio * cantidad de cada item
    total = sum(item["precio"] * item["cantidad"] for item in items_orden)
    
    # Mostrar resumen final de la orden antes de confirmar
    print("\n" + "━" * 50)
    print("RESUMEN DE LA ORDEN".center(50))
    print("━" * 50)
    for item in items_orden:
        subtotal = item["precio"] * item["cantidad"]
        print(f"{item['cantidad']}x {item['nombre']:<30} ${subtotal:>6.2f}")
    print("━" * 50)
    print(f"{'TOTAL:':<36} ${total:>6.2f}")
    print("━" * 50)
    
    # Confirmación de la orden antes de guardar
    try:
        confirmar = input("\n¿Confirmar orden? (s/n): ").lower()
    except KeyboardInterrupt:
        print('No pasaras 🧙')
    if confirmar == 's':
        # Crear factura con ID, fecha actual, items y total
        factura = {
            "id": generarIdFactura(),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": items_orden,
            "total": total
        }
        
        # Guardar factura en el JSON
        datos["facturas"].append(factura)
        write_json(DATA_FILE, datos)
        
        print(f"\nOrden registrada exitosamente! ID Factura: {factura['id']}")
    else:
        print("\nOrden cancelada.")
    
    pausar()


def verOrdenes():
    """Muestra todas las órdenes/facturas"""
    limpiar()
    print("━" * 50)
    print("━━" + "ÓRDENES REGISTRADAS".center(46) + "━━")
    print("━" * 50)
    
    # Carga todas las facturas del archivo
    datos = read_json(DATA_FILE)
    facturas = datos.get("facturas", [])
    
    if not facturas:
        print("\nNo hay órdenes registradas.")
        pausar()
        return
    
    # Recorre cada factura y muestra resumen
    for factura in facturas:
        print(f"\nFactura #{factura['id']} - {factura['fecha']}")
        print(f"   Total: ${factura['total']:.2f}")
        print(f"   Items: {len(factura['items'])}")
    
    pausar()


def verPizzas():
    """Muestra todas las pizzas"""
    limpiar()
    print("━" * 50)
    print("━━" + "LISTA DE PIZZAS".center(46) + "━━")
    print("━" * 50)
    
    datos = read_json(DATA_FILE)
    pizzas = datos.get("pizzas", {})
    
    if not pizzas:
        print("\nNo hay pizzas registradas.")
    else:
        # Encabezado de tabla de pizzas
        print(f"\n{'ID':<5} {'NOMBRE':<25} {'PRECIO':<10} {'ESTADO'}")
        print("━" * 50)
        for id_pizza, pizza in pizzas.items():
            estado = "Activa" if pizza["activa"] else "Inactiva"
            print(f"{id_pizza:<5} {pizza['nombre']:<25} ${pizza['precio']:<9.2f} {estado}")
    
    pausar()


def agregarPizza():
    """Agrega una nueva pizza al menú"""
    limpiar()
    print("━" * 50)
    print("━━" + "AGREGAR PIZZA".center(46) + "━━")
    print("━" * 50)
    
    # Pide nombre y precio de la nueva pizza
    nombre = validarInput("\nNombre de la pizza: ", 'str')
    precio = validarInput("Precio: $", 'float')
    
    if precio <= 0:
        print("\nEl precio debe ser mayor a 0.")
        pausar()
        return
    
    datos = read_json(DATA_FILE)
    # Nuevo ID simple basado en cantidad actual de pizzas
    nuevo_id = str(len(datos["pizzas"]) + 1)
    
    # Registra la nueva pizza como activa
    datos["pizzas"][nuevo_id] = {
        "nombre": nombre,
        "precio": precio,
        "activa": True
    }
    
    write_json(DATA_FILE, datos)
    print(f"\nPizza '{nombre}' agregada exitosamente con ID {nuevo_id}!")
    pausar()


def desactivarPizza():
    """Desactiva/activa una pizza"""
    limpiar()
    print("━" * 50)
    print("━━" + "ACTIVAR/DESACTIVAR PIZZA".center(46) + "━━")
    print("━" * 50)
    
    datos = read_json(DATA_FILE)
    pizzas = datos.get("pizzas", {})
    
    # Muestra listado de pizzas con su estado actual
    print(f"\n{'ID':<5} {'NOMBRE':<25} {'ESTADO'}")
    print("━" * 50)
    for id_pizza, pizza in pizzas.items():
        estado = "Activa" if pizza["activa"] else "Inactiva"
        print(f"{id_pizza:<5} {pizza['nombre']:<25} {estado}")
    
    # Pide el ID de la pizza para cambiar su estado
    id_pizza = validarInput("\nID de la pizza a cambiar estado: ", 'str')
    
    if id_pizza not in pizzas:
        print("\nPizza no encontrada.")
        pausar()
        return
    
    # Alterna el valor booleando de 'activa'
    pizzas[id_pizza]["activa"] = not pizzas[id_pizza]["activa"]
    write_json(DATA_FILE, datos)
    
    estado_nuevo = "activada" if pizzas[id_pizza]["activa"] else "desactivada"
    print(f"\nPizza '{pizzas[id_pizza]['nombre']}' {estado_nuevo} exitosamente!")
    pausar()


def verAdicionales():
    """Muestra todos los adicionales"""
    limpiar()
    print("━" * 50)
    print("━━" + "LISTA DE ADICIONALES".center(46) + "━━")
    print("━" * 50)
    
    datos = read_json(DATA_FILE)
    adicionales = datos.get("adicionales", {})
    
    if not adicionales:
        print("\nNo hay adicionales registrados.")
    else:
        # Encabezado de tabla de adicionales
        print(f"\n{'ID':<5} {'NOMBRE':<25} {'PRECIO':<10} {'ESTADO'}")
        print("━" * 50)
        for id_adic, adic in adicionales.items():
            estado = "Activo" if adic["activo"] else "Inactivo"
            print(f"{id_adic:<5} {adic['nombre']:<25} ${adic['precio']:<9.2f} {estado}")
    
    pausar()


def agregarAdicional():
    """Agrega un nuevo adicional"""
    limpiar()
    print("━" * 50)
    print("━━" + "AGREGAR ADICIONAL".center(46) + "━━")
    print("━" * 50)
    
    # Pide nombre y precio del adicional
    nombre = validarInput("\nNombre del adicional: ", 'str')
    precio = validarInput("Precio: $", 'float')
    
    if precio <= 0:
        print("\nEl precio debe ser mayor a 0.")
        pausar()
        return
    
    datos = read_json(DATA_FILE)
    # Nuevo ID basado en la cantidad actual de adicionales
    nuevo_id = str(len(datos["adicionales"]) + 1)
    
    # Crea el adicional como activo
    datos["adicionales"][nuevo_id] = {
        "nombre": nombre,
        "precio": precio,
        "activo": True
    }
    
    write_json(DATA_FILE, datos)
    print(f"\nAdicional '{nombre}' agregado exitosamente con ID {nuevo_id}!")
    pausar()


def desactivarAdicional():
    """Desactiva/activa un adicional"""
    limpiar()
    print("━" * 50)
    print("━━" + "ACTIVAR/DESACTIVAR ADICIONAL".center(46) + "━━")
    print("━" * 50)
    
    datos = read_json(DATA_FILE)
    adicionales = datos.get("adicionales", {})
    
    # Muestra listado de adicionales con su estado
    print(f"\n{'ID':<5} {'NOMBRE':<25} {'ESTADO'}")
    print("━" * 50)
    for id_adic, adic in adicionales.items():
        estado = "Activo" if adic["activo"] else "Inactivo"
        print(f"{id_adic:<5} {adic['nombre']:<25} {estado}")
    
    # Pide ID del adicional para alternar su estado
    id_adic = validarInput("\nID del adicional a cambiar estado: ", 'str')
    
    if id_adic not in adicionales:
        print("\nAdicional no encontrado.")
        pausar()
        return
    
    # Alterna 'activo'
    adicionales[id_adic]["activo"] = not adicionales[id_adic]["activo"]
    write_json(DATA_FILE, datos)
    
    estado_nuevo = "activado" if adicionales[id_adic]["activo"] else "desactivado"
    print(f"\nAdicional '{adicionales[id_adic]['nombre']}' {estado_nuevo} exitosamente!")
    pausar()


def verReportesVentas():
    """Menú de reportes de ventas con opciones de ordenamiento y filtrado"""
    # Bucle de menú de reportes hasta que el usuario vuelva al menú admin
    while True:
        limpiar()
        opciones = [
            "Ver todas las facturas",
            "Ordenar por monto (menor a mayor)",
            "Ordenar por monto (mayor a menor)",
            "Ordenar por fecha (más antigua a más reciente)",
            "Ordenar por fecha (más reciente a más antigua)",
            "Filtrar por rango de fechas",
            "Regresar al menú admin"
        ]
        opcion = imprimirMenus("REPORTES DE VENTAS", opciones)
        
        # Se leen facturas en cada iteración para tener datos actualizados
        datos = read_json(DATA_FILE)
        facturas = datos.get("facturas", [])
        
        if not facturas and opcion != 7:
            print("\nNo hay facturas registradas.")
            pausar()
            continue
        
        # Uso de pattern matching para seleccionar acción de reporte
        match opcion:
            case 1:
                mostrarFacturas(facturas, "TODAS LAS FACTURAS")
            case 2:
                facturas_ordenadas = sorted(facturas, key=lambda x: x["total"])
                mostrarFacturas(facturas_ordenadas, "FACTURAS ORDENADAS POR MONTO (MENOR A MAYOR)")
            case 3:
                facturas_ordenadas = sorted(facturas, key=lambda x: x["total"], reverse=True)
                mostrarFacturas(facturas_ordenadas, "FACTURAS ORDENADAS POR MONTO (MAYOR A MENOR)")
            case 4:
                facturas_ordenadas = sorted(facturas, key=lambda x: x["fecha"])
                mostrarFacturas(facturas_ordenadas, "FACTURAS ORDENADAS POR FECHA (ANTIGUA → RECIENTE)")
            case 5:
                facturas_ordenadas = sorted(facturas, key=lambda x: x["fecha"], reverse=True)
                mostrarFacturas(facturas_ordenadas, "FACTURAS ORDENADAS POR FECHA (RECIENTE → ANTIGUA)")
            case 6:
                filtrarPorFechas(facturas)
            case 7:
                # Opción para regresar al menú administrador
                break


def mostrarFacturas(facturas, titulo):
    """Muestra una lista de facturas con formato bonito"""
    limpiar()
    print("━" * 80)
    print("━━" + titulo.center(76) + "━━")
    print("━" * 80)
    
    if not facturas:
        print("\nNo hay facturas para mostrar.")
        pausar()
        return
    
    # Calcula el total de ventas del conjunto de facturas
    total_ventas = sum(f["total"] for f in facturas)
    
    # Encabezado de tabla de facturas
    print(f"\n{'ID':<6} {'FECHA':<20} {'ITEMS':<8} {'TOTAL':>12}")
    print("━" * 80)
    
    for factura in facturas:
        print(f"{factura['id']:<6} {factura['fecha']:<20} {len(factura['items']):<8} ${factura['total']:>11.2f}")
    
    print("━" * 80)
    print(f"{'TOTAL DE VENTAS:':<35} ${total_ventas:>11.2f}")
    print(f"{'NÚMERO DE FACTURAS:':<35} {len(facturas):>12}")
    print("━" * 80)
    
    # Preguntar si quiere ver detalles de una factura específica
    try:
        ver_detalle = input("\n¿Ver detalles de alguna factura? (ID o 'n' para salir): ")
    except KeyboardInterrupt:
        print('No pasaras 🧙')
    if ver_detalle.lower() != 'n':
        try:
            id_factura = int(ver_detalle)
            # Busca la factura con ese ID dentro de la lista
            factura_detalle = next((f for f in facturas if f["id"] == id_factura), None)
            if factura_detalle:
                mostrarDetalleFactura(factura_detalle)
            else:
                print("\nFactura no encontrada.")
                pausar()
        except ValueError:
            print("\nID inválido.")
            pausar()


def mostrarDetalleFactura(factura):
    """Muestra el detalle completo de una factura"""
    limpiar()
    print("━" * 80)
    print("━━" + f"DETALLE FACTURA #{factura['id']}".center(76) + "━━")
    print("━" * 80)
    print(f"\nFecha: {factura['fecha']}")
    print(f"\n{'CANT':<6} {'DESCRIPCIÓN':<45} {'PRECIO':<12} {'SUBTOTAL':>12}")
    print("━" * 80)
    
    # Recorre cada item de la factura y calcula el subtotal
    for item in factura["items"]:
        subtotal = item["precio"] * item["cantidad"]
        print(f"{item['cantidad']:<6} {item['nombre']:<42} ${item['precio']:<11.2f} ${subtotal:>11.2f}")
    
    print("━" * 80)
    print(f"{'TOTAL:':<66} ${factura['total']:>11.2f}")
    print("━" * 80)
    pausar()


def filtrarPorFechas(facturas):
    """Filtra facturas por rango de fechas"""
    limpiar()
    print("━" * 80)
    print("━━" + "FILTRAR POR RANGO DE FECHAS".center(76) + "━━")
    print("━" * 80)
    
    print("\nFormato de fecha: YYYY-MM-DD (ejemplo: 2025-12-09)")
    # Se leen las fechas como string y luego se convierten a datetime
    fecha_inicio_str = validarInput("Fecha de inicio: ", 'str')
    fecha_fin_str = validarInput("Fecha de fin: ", 'str')
    
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
        
        # Ajustar fecha_fin para incluir todo el día (hasta las 23:59:59)
        fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59)
        
        if fecha_inicio > fecha_fin:
            print("\nLa fecha de inicio debe ser anterior a la fecha de fin.")
            pausar()
            return
        
        # Recorre las facturas y se queda solo con las que están en el rango
        facturas_filtradas = []
        for factura in facturas:
            fecha_factura = datetime.strptime(factura["fecha"], "%Y-%m-%d %H:%M:%S")
            if fecha_inicio <= fecha_factura <= fecha_fin:
                facturas_filtradas.append(factura)
        
        titulo = f"FACTURAS DEL {fecha_inicio_str} AL {fecha_fin_str}"
        mostrarFacturas(facturas_filtradas, titulo)
        
    except ValueError:
        # Manejo de formato incorrecto de fecha
        print("\nFormato de fecha inválido. Use YYYY-MM-DD")
        pausar()


def maincoso():
    # Punto de entrada principal del sistema de pizzería
    inicializarDatos()
    
    while True:
        limpiar()
        print('Bienvenido al Sistema de Gestión de Pizzería\n')
        # Menú principal: mesero, admin o salir
        opcion = imprimirMenus("MENÚ PRINCIPAL", menuInicio.values())
        
        match opcion:
            case 1:
                mesero()
            case 2:
                admin()
            case 3:
                print("\n¡Gracias por usar el sistema! Hasta pronto...")
                time.sleep(1)
                break
    return True


def mesero():
    # Submenú para funcionalidades del mesero
    while True:
        opcion = imprimirMenus('MENÚ MESERO', menuPizzas.values())
        
        match opcion:
            case 1:
                tomarOrden()
            case 2:
                verOrdenes()
            case 3:
                print("\n↩Regresando al menú principal...")
                time.sleep(0.5)
                break


def admin():
    # Submenú para funcionalidades del administrador
    while True:
        opcion = imprimirMenus('MENÚ ADMINISTRADOR', menuAdmin.values())
        
        match opcion:
            case 1:
                verPizzas()
            case 2:
                agregarPizza()
            case 3:
                desactivarPizza()
            case 4:
                adicionales_menu()
            case 5:
                verReportesVentas()
            case 6:
                print("\n↩Regresando al menú principal...")
                time.sleep(0.5)
                break


def adicionales_menu():
    # Submenú específico para gestión de adicionales
    while True:
        opcion = imprimirMenus('MENÚ ADICIONALES', menuAdicionales.values())
        
        match opcion:
            case 1:
                verAdicionales()
            case 2:
                agregarAdicional()
            case 3:
                desactivarAdicional()
            case 4:
                print("\n↩Regresando al menú admin...")
                time.sleep(0.5)
                break
