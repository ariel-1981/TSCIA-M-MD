import csv
import os
import glob
import json
from typing import List, Dict

class CSVManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.fieldnames = []
        self._load_fieldnames()
    
    def _load_fieldnames(self):
        """Carga los nombres de las columnas del CSV"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.fieldnames = reader.fieldnames or []
    
    # CREATE
    def create(self, data: Dict) -> bool:
        """Agrega un nuevo registro al CSV con ID autoincremental"""
        try:
            # Si tiene campo 'id', generar el siguiente ID automáticamente
            if 'id' in self.fieldnames:
                all_data = self.read_all()
                if all_data:
                    # Obtener el ID máximo actual
                    ids_numericos = []
                    for row in all_data:
                        try:
                            ids_numericos.append(int(row['id']))
                        except (ValueError, KeyError):
                            pass
                    
                    if ids_numericos:
                        nuevo_id = max(ids_numericos) + 1
                    else:
                        nuevo_id = 1
                else:
                    nuevo_id = 1
                
                data['id'] = str(nuevo_id)
                print(f"→ ID asignado automáticamente: {nuevo_id}")
            
            file_exists = os.path.exists(self.filename)
            with open(self.filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
            print(f"✓ Registro creado exitosamente en {self.filename}")
            return True
        except Exception as e:
            print(f"✗ Error al crear registro: {e}")
            return False
    
    # READ
    def read_all(self) -> List[Dict]:
        """Lee todos los registros del CSV"""
        try:
            if not os.path.exists(self.filename):
                print(f"⚠ El archivo {self.filename} no existe")
                return []
            
            with open(self.filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            print(f"✗ Error al leer registros: {e}")
            return []
    
    def read_by_field(self, field: str, value: str) -> List[Dict]:
        """Busca registros por un campo específico"""
        all_data = self.read_all()
        return [row for row in all_data if row.get(field) == value]
    
    # UPDATE
    def update(self, field: str, value: str, new_data: Dict) -> bool:
        """Actualiza registros que coincidan con el criterio"""
        try:
            all_data = self.read_all()
            updated = False
            
            for row in all_data:
                if row.get(field) == value:
                    row.update(new_data)
                    updated = True
            
            if updated:
                self._write_all(all_data)
                print(f"✓ Registro(s) actualizado(s) en {self.filename}")
                return True
            else:
                print(f"⚠ No se encontró ningún registro con {field}={value}")
                return False
        except Exception as e:
            print(f"✗ Error al actualizar: {e}")
            return False
    
    # DELETE
    def delete(self, field: str, value: str) -> bool:
        """Elimina registros que coincidan con el criterio"""
        try:
            all_data = self.read_all()
            original_count = len(all_data)
            filtered_data = [row for row in all_data if row.get(field) != value]
            
            if len(filtered_data) < original_count:
                self._write_all(filtered_data)
                deleted = original_count - len(filtered_data)
                print(f"✓ {deleted} registro(s) eliminado(s) de {self.filename}")
                return True
            else:
                print(f"⚠ No se encontró ningún registro con {field}={value}")
                return False
        except Exception as e:
            print(f"✗ Error al eliminar: {e}")
            return False
    
    def _write_all(self, data: List[Dict]):
        """Escribe todos los datos al CSV"""
        with open(self.filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)
    
    def display_all(self):
        """Muestra todos los registros de forma legible"""
        data = self.read_all()
        if not data:
            print(f"\n{self.filename} está vacío o no existe\n")
            return
        
        print(f"\n{'='*60}")
        print(f"Contenido de {self.filename}")
        print('='*60)
        for i, row in enumerate(data, 1):
            print(f"\nRegistro {i}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
        print('='*60 + '\n')
    
    def export_to_json(self, output_filename: str = None) -> bool:
        """Exporta los datos del CSV a formato JSON"""
        try:
            data = self.read_all()
            if not data:
                print(f"⚠ No hay datos para exportar en {self.filename}")
                return False
            
            # Si no se especifica nombre, usar el mismo nombre con extensión .json
            if not output_filename:
                output_filename = self.filename.replace('.csv', '.json')
            
            with open(output_filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            
            print(f"✓ Datos exportados exitosamente a {output_filename}")
            print(f"  Total de registros: {len(data)}")
            return True
        except Exception as e:
            print(f"✗ Error al exportar a JSON: {e}")
            return False


def obtener_archivos_csv() -> List[str]:
    """Obtiene todos los archivos CSV en el directorio actual"""
    archivos = glob.glob("*.csv")
    return sorted(archivos)


def menu_principal():
    """Menú interactivo para el sistema CRUD"""
    while True:
        # Buscar todos los CSV en la carpeta
        archivos_csv = obtener_archivos_csv()
        
        print("\n" + "="*50)
        print("SISTEMA CRUD - GESTIÓN DE CSVs")
        print("="*50)
        
        if not archivos_csv:
            print("⚠ No se encontraron archivos CSV en el directorio actual")
            print("="*50)
            opcion = input("\n¿Desea crear un nuevo archivo CSV? (s/n): ").strip().lower()
            if opcion == 's':
                crear_nuevo_csv()
                continue
            else:
                print("\n¡Hasta luego!")
                break
        
        print("Archivos CSV disponibles:")
        for i, archivo in enumerate(archivos_csv, 1):
            num_registros = len(CSVManager(archivo).read_all())
            print(f"{i}. {archivo} ({num_registros} registros)")
        
        print("="*50)
        print("0. Salir")
        print("N. Crear nuevo archivo CSV")
        print("="*50)
        
        opcion = input("Seleccione un archivo (número) o N para nuevo: ").strip()
        
        if opcion == '0':
            print("\n¡Hasta luego!")
            break
        
        if opcion.upper() == 'N':
            crear_nuevo_csv()
            continue
        
        try:
            indice = int(opcion) - 1
            if 0 <= indice < len(archivos_csv):
                archivo_seleccionado = archivos_csv[indice]
                manager = CSVManager(archivo_seleccionado)
                menu_crud(manager)
            else:
                print("⚠ Opción inválida")
        except ValueError:
            print("⚠ Debe ingresar un número válido")


def crear_nuevo_csv():
    """Crea un nuevo archivo CSV con campos personalizados"""
    print("\n" + "="*50)
    print("CREAR NUEVO ARCHIVO CSV")
    print("="*50)
    
    nombre_archivo = input("Nombre del archivo (sin extensión): ").strip()
    if not nombre_archivo:
        print("⚠ Nombre inválido")
        return
    
    nombre_archivo = nombre_archivo + ".csv"
    
    if os.path.exists(nombre_archivo):
        print(f"⚠ El archivo {nombre_archivo} ya existe")
        return
    
    print("\nIngrese los nombres de las columnas separados por comas")
    print("Ejemplo: id,nombre,precio,stock")
    columnas = input("Columnas: ").strip()
    
    if not columnas:
        print("⚠ Debe especificar al menos una columna")
        return
    
    fieldnames = [col.strip() for col in columnas.split(',')]
    
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        print(f"\n✓ Archivo {nombre_archivo} creado exitosamente")
    except Exception as e:
        print(f"✗ Error al crear archivo: {e}")


def menu_crud(manager: CSVManager):
    """Menú de operaciones CRUD"""
    while True:
        print(f"\n{'='*50}")
        print(f"Gestionando: {manager.filename}")
        if manager.fieldnames:
            print(f"Campos: {', '.join(manager.fieldnames)}")
        print('='*50)
        print("1. Ver todos los registros")
        print("2. Buscar registro")
        print("3. Crear nuevo registro")
        print("4. Actualizar registro")
        print("5. Eliminar registro")
        print("6. Exportar a JSON")
        print("0. Volver al menú principal")
        print('='*50)
        
        opcion = input("Opción: ").strip()
        
        if opcion == '0':
            break
        elif opcion == '1':
            manager.display_all()
        elif opcion == '2':
            buscar_registro(manager)
        elif opcion == '3':
            crear_registro(manager)
        elif opcion == '4':
            actualizar_registro(manager)
        elif opcion == '5':
            eliminar_registro(manager)
        elif opcion == '6':
            exportar_a_json(manager)
        else:
            print("⚠ Opción inválida")


def buscar_registro(manager: CSVManager):
    """Busca registros por un campo"""
    if not manager.fieldnames:
        print("⚠ El archivo no tiene campos definidos")
        return
    
    print(f"\nCampos disponibles: {', '.join(manager.fieldnames)}")
    campo = input("Campo a buscar: ").strip()
    
    if campo not in manager.fieldnames:
        print(f"⚠ El campo '{campo}' no existe en este archivo")
        return
    
    valor = input(f"Valor de {campo}: ").strip()
    
    resultados = manager.read_by_field(campo, valor)
    
    if resultados:
        print(f"\n✓ Se encontraron {len(resultados)} registro(s):")
        for i, row in enumerate(resultados, 1):
            print(f"\nRegistro {i}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
    else:
        print(f"\n⚠ No se encontraron registros con {campo}={valor}")


def crear_registro(manager: CSVManager):
    """Crea un nuevo registro"""
    if not manager.fieldnames:
        print("⚠ No se pueden determinar los campos del archivo")
        return
    
    print(f"\nCrear nuevo registro en {manager.filename}")
    
    # Determinar qué campos solicitar (excluir 'id' si existe)
    campos_a_solicitar = [field for field in manager.fieldnames if field != 'id']
    
    if 'id' in manager.fieldnames:
        print("(El ID se asignará automáticamente)")
        print(f"Campos a completar: {', '.join(campos_a_solicitar)}")
    else:
        print(f"Campos requeridos: {', '.join(manager.fieldnames)}")
        campos_a_solicitar = manager.fieldnames
    
    print()
    
    nuevo_registro = {}
    
    # Solicitar solo los campos que no son ID
    for field in campos_a_solicitar:
        valor = input(f"{field}: ").strip()
        nuevo_registro[field] = valor
    
    manager.create(nuevo_registro)


def actualizar_registro(manager: CSVManager):
    """Actualiza un registro existente"""
    if not manager.fieldnames:
        print("⚠ El archivo no tiene campos definidos")
        return
    
    print(f"\nCampos disponibles: {', '.join(manager.fieldnames)}")
    campo_busqueda = input("Campo para buscar el registro a actualizar: ").strip()
    
    if campo_busqueda not in manager.fieldnames:
        print(f"⚠ El campo '{campo_busqueda}' no existe")
        return
    
    valor_busqueda = input(f"Valor de {campo_busqueda}: ").strip()
    
    # Mostrar registro actual
    registros = manager.read_by_field(campo_busqueda, valor_busqueda)
    if not registros:
        print(f"\n⚠ No se encontró ningún registro con {campo_busqueda}={valor_busqueda}")
        return
    
    print("\nRegistro actual:")
    for key, value in registros[0].items():
        print(f"  {key}: {value}")
    
    print("\nIngrese los nuevos valores (deje en blanco para mantener el valor actual):")
    nuevos_datos = {}
    for field in manager.fieldnames:
        valor = input(f"{field} [{registros[0].get(field)}]: ").strip()
        if valor:
            nuevos_datos[field] = valor
    
    if nuevos_datos:
        manager.update(campo_busqueda, valor_busqueda, nuevos_datos)
    else:
        print("⚠ No se realizaron cambios")


def eliminar_registro(manager: CSVManager):
    """Elimina un registro"""
    if not manager.fieldnames:
        print("⚠ El archivo no tiene campos definidos")
        return
    
    print(f"\nCampos disponibles: {', '.join(manager.fieldnames)}")
    campo = input("Campo para identificar el registro a eliminar: ").strip()
    
    if campo not in manager.fieldnames:
        print(f"⚠ El campo '{campo}' no existe")
        return
    
    valor = input(f"Valor de {campo}: ").strip()
    
    # Mostrar qué se va a eliminar
    registros = manager.read_by_field(campo, valor)
    if registros:
        print(f"\n⚠ Se eliminará(n) {len(registros)} registro(s):")
        for row in registros:
            print(row)
        
        confirmar = input("\n¿Confirmar eliminación? (s/n): ").strip().lower()
        if confirmar == 's':
            manager.delete(campo, valor)
        else:
            print("Eliminación cancelada")
    else:
        print(f"\n⚠ No se encontró ningún registro con {campo}={valor}")


def exportar_a_json(manager: CSVManager):
    """Exporta la tabla actual a formato JSON"""
    print(f"\n{'='*50}")
    print("EXPORTAR A JSON")
    print('='*50)
    
    # Sugerir nombre de archivo por defecto
    nombre_sugerido = manager.filename.replace('.csv', '.json')
    print(f"Nombre sugerido: {nombre_sugerido}")
    
    nombre_archivo = input("Nombre del archivo JSON (Enter para usar sugerido): ").strip()
    
    if not nombre_archivo:
        nombre_archivo = nombre_sugerido
    
    # Asegurar que tenga extensión .json
    if not nombre_archivo.endswith('.json'):
        nombre_archivo += '.json'
    
    # Confirmar si el archivo ya existe
    if os.path.exists(nombre_archivo):
        confirmar = input(f"⚠ El archivo {nombre_archivo} ya existe. ¿Sobrescribir? (s/n): ").strip().lower()
        if confirmar != 's':
            print("Exportación cancelada")
            return
    
    manager.export_to_json(nombre_archivo)


if __name__ == "__main__":
    menu_principal()