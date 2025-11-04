# 📊 Editor de Archivos CSV

Script interactivo en Python para leer, modificar y exportar archivos CSV en múltiples formatos.

## 📋 Descripción

Esta herramienta te permite cargar un archivo CSV, realizar modificaciones (agregar, eliminar o modificar filas y columnas) y exportar los resultados en tres formatos diferentes: CSV, JSON o Excel.

## ✨ Características

- ✅ Lectura de archivos CSV
- ➕ Agregar nuevas filas con valores personalizados
- 🗑️ Eliminar filas por índice
- ✏️ Modificar valores de filas existentes
- 📊 Agregar columnas de ejemplo
- 👀 Visualizar el DataFrame en cualquier momento
- 💾 Exportar en tres formatos:
  - CSV (`.csv`)
  - JSON (`.json`)
  - Excel (`.xlsx`)

## 🔧 Requisitos

### Librerías necesarias

```bash
pip install pandas openpyxl
```

- **pandas**: Para manipulación de datos
- **openpyxl**: Para exportación a Excel

## 🚀 Uso

### 1. Ejecutar el script

```bash
python editor_csv.py
```

### 2. Ingresar el nombre del archivo

El script te pedirá el nombre del archivo CSV a cargar:

```
📄 Ingresá el nombre del archivo CSV (ejemplo: datos.csv): 
```

Si el archivo no existe, se mostrará una lista de archivos disponibles en el directorio actual.

### 3. Menú de modificaciones

Una vez cargado el archivo, aparecerá un menú interactivo:

```
🔧 Menú de modificaciones:
1 - Agregar una fila
2 - Eliminar una fila
3 - Modificar una fila existente
4 - Agregar columna de ejemplo
5 - Ver DataFrame
0 - Terminar modificaciones
```

#### Opciones del menú:

- **Opción 1**: Agrega una nueva fila solicitando valores para cada columna
- **Opción 2**: Elimina una fila especificando su índice
- **Opción 3**: Modifica valores de una fila existente (dejá vacío para mantener el valor actual)
- **Opción 4**: Agrega una columna numérica de ejemplo llamada "Nueva_Columna"
- **Opción 5**: Muestra el DataFrame completo en consola
- **Opción 0**: Finaliza las modificaciones y continúa con la exportación

### 4. Exportar el archivo

Después de terminar las modificaciones, elegí el formato de salida:

```
¿En qué formato querés guardar el archivo modificado?
1 - CSV
2 - JSON
3 - Excel
Elegí una opción (1, 2 o 3):
```

Los archivos se guardan con los siguientes nombres:
- CSV: `archivo_modificado.csv`
- JSON: `archivo_modificado.json`
- Excel: `archivo_modificado.xlsx`

## 📝 Ejemplo de uso

```
📄 Ingresá el nombre del archivo CSV (ejemplo: datos.csv): ventas.csv

✅ Archivo leído correctamente.

Vista previa del DataFrame:
   Producto  Precio  Cantidad
0  Laptop    1500    5
1  Mouse     25      20
2  Teclado   80      15

🔧 Menú de modificaciones:
1 - Agregar una fila
...
Elegí una opción: 1

👉 Ingresá los valores para una nueva fila:
Producto: Monitor
Precio: 300
Cantidad: 10

✅ Fila agregada correctamente.

Elegí una opción: 0

¿En qué formato querés guardar el archivo modificado?
1 - CSV
2 - JSON
3 - Excel
Elegí una opción (1, 2 o 3): 3

✅ Archivo guardado como Excel: 'archivo_modificado.xlsx'
```

## 🛠️ Estructura del código

El script está organizado en las siguientes secciones:

1. **Lectura del archivo**: Carga el CSV y muestra una vista previa
2. **Funciones de modificación**:
   - `agregar_fila(df)`: Agrega una nueva fila
   - `eliminar_fila(df)`: Elimina una fila por índice
   - `modificar_fila(df)`: Modifica valores de una fila existente
   - `mostrar_menu_modificacion(df)`: Menú interactivo principal
3. **Exportación**: Guarda el DataFrame en el formato seleccionado

## ⚠️ Notas importantes

- El archivo CSV debe estar en el mismo directorio que el script, o especificá la ruta completa
- Los índices de las filas comienzan en 0
- Al modificar una fila, podés dejar campos vacíos para mantener el valor actual
- El archivo Excel se guarda en formato `.xlsx` (Excel 2007+)
- Si el archivo de salida ya existe, será sobrescrito
