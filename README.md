# 🍕 Sistema de Gestión de Pizzería

Este proyecto es una aplicación de consola en **Python** diseñada para gestionar pedidos, pizzas, adicionales y facturas de una pizzería.  
Permite a **meseros** tomar órdenes de clientes y a **administradores** administrar el menú, adicionales y generar reportes de ventas.  
La persistencia de datos se maneja mediante archivos **JSON**, lo que hace que el sistema sea completamente funcional sin base de datos externa.

---

## 📋 Características principales

### 👨‍🍳 Modo Mesero
- Tomar órdenes de clientes (con selección de pizzas y adicionales).
- Generar facturas automáticas con ID único y total calculado.
- Consultar todas las órdenes registradas.

### 🧑‍💼 Modo Administrador
- Visualizar, agregar, activar o desactivar **pizzas**.
- Visualizar, agregar, activar o desactivar **adicionales**.
- Generar **reportes de ventas**:
  - Mostrar todas las facturas.
  - Ordenar facturas por monto o fecha (ascendente o descendente).
  - Filtrar facturas por rango de fechas.
- Consultar el detalle individual de cada factura.

### 💾 Persistencia
- Todos los datos se almacenan en `./data/datadata.json`:
  - Pizzas
  - Adicionales
  - Facturas (ventas)

---

## 🧱 Estructura del proyecto

pizzeria/
│
├── data/
│ └── datadata.json # Archivo con los datos persistentes
│
├── utils/
│ ├── menus.py # Contiene los diccionarios de menús
│ ├── jsonFileHandler.py # Lectura/escritura del archivo JSON
│
├── main.py (o maincoso.py) # Archivo principal del sistema
│
└── README.md


---

## ⚙️ Requisitos

- Python **3.10+** (necesario para usar `match case`)
- Sistema operativo compatible con comandos de consola (`cls` o `clear`)

---

## 🚀 Instalación y ejecución

1. **Clona el repositorio:**

git clone https://github.com/Angelux331/Pizzeria-Restaurant-Project.git
cd pizzeria-system


2. **Ejecuta el programa principal:**


3. **Selecciona el modo:**
   - `1` para **Mesero**  
   - `2` para **Administrador**  
   - `3` para salir del sistema

---

## 🧮 Ejemplo de flujo

1. Inicia el programa.
2. Inicia sesión como **Mesero**.
3. Selecciona "Tomar orden".
4. Agrega pizzas y adicionales.
5. Confirma el pedido → se genera una factura.
6. (Opcional) En el modo **Administrador**, revisa las ventas y genera reportes.

---

## 🧰 Funciones destacadas

| Función | Descripción |
|----------|-------------|
| `tomarOrden()` | Permite registrar una orden completa (pizzas, adicionales, total). |
| `verOrdenes()` | Muestra todas las facturas registradas. |
| `verReportesVentas()` | Genera reportes y filtros de ventas. |
| `agregarPizza()` / `agregarAdicional()` | Agrega nuevos productos al menú. |
| `desactivarPizza()` / `desactivarAdicional()` | Cambia el estado activo/inactivo de un producto. |
| `inicializarDatos()` | Crea la estructura base del archivo JSON si no existe. |

---

## 🧠 Notas técnicas

- Se usa manejo de errores para entradas inválidas y Ctrl+C.
- Las fechas se manejan con `datetime` en formato `YYYY-MM-DD HH:MM:SS`.
- Los reportes de ventas se ordenan y filtran dinámicamente sin librerías externas.
- Menús y textos adaptados a español, con interfaz amigable en consola.

