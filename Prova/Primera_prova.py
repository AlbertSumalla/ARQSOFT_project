from typing import Dict, Tuple, Union
import re

## @class Celda
#  @brief Representa una celda individual en la hoja de cálculo.
#  @details Maneja el contenido, valor calculado y dependencias de una celda identificada por su coordenada (ej. "A1").
class Celda:
    def __init__(self, coord: str):
        ## @var coord
        #  @brief Coordenada de la celda en formato "A1", "B2", etc.
        self.coord = coord
        ## @var contenido
        #  @brief Contenido crudo de la celda (texto, número o fórmula).
        self.contenido = None
        ## @var valor
        #  @brief Valor calculado del contenido (número, texto o resultado de fórmula).
        self.valor = None
        ## @var dependencias
        #  @brief Conjunto de coordenadas de celdas de las que depende esta celda.
        self.dependencias = set()

    ## @brief Establece el contenido de la celda y valida dependencias.
    #  @param contenido Texto ingresado (número, texto o fórmula).
    #  @param hoja Instancia de HojaCalculo para acceder a otras celdas.
    #  @exception ValueError Si se detecta una dependencia circular.
    def set_contenido(self, contenido: str, hoja) -> None:
        self.contenido = contenido
        if contenido and contenido.startswith("="):
            self.dependencias = self._extraer_dependencias(contenido)
            if self._detectar_circularidad(hoja):
                raise ValueError(f"Dependencia circular detectada en {self.coord}")
        self.actualizar_valor(hoja)
    
    ## @brief Extrae las dependencias de una fórmula.
    #  @param formula Texto de la fórmula sin el "=" inicial.
    #  @return Conjunto de coordenadas referenciadas (ej. {"A1", "B2"}).
    def _extraer_dependencias(self, formula: str) -> set:
        pattern = r"[A-Z]+[1-9]\d*"  # Expresión regular para encontrar referencias como A1, B23, etc.
        return set(re.findall(pattern, formula))
    
    ## @brief Detecta si hay dependencias circulares.
    #  @param hoja Instancia de HojaCalculo.
    #  @param visitados Conjunto de celdas ya visitadas (para recursión).
    #  @return True si hay circularidad, False si no.
    def _detectar_circularidad(self, hoja, visitados=None) -> bool:
        if visitados is None:
            visitados = set()
        if self.coord in visitados:
            return True
        visitados.add(self.coord)
        for dep in self.dependencias:
            celda_dep = hoja.get_celda(dep)
            if celda_dep and celda_dep.contenido and celda_dep.contenido.startswith("="):
                if celda_dep._detectar_circularidad(hoja, visitados.copy()):
                    return True
        return False
    
    ## @brief Actualiza el valor de la celda basado en su contenido.
    #  @param hoja Instancia de HojaCalculo para evaluar fórmulas.
    def actualizar_valor(self, hoja) -> None:
        if not self.contenido:
            self.valor = None
        elif self.contenido.startswith("="):
            self.valor = hoja.operaciones.evaluar_formula(self.contenido[1:], self)
        else:
            try:
                # Intenta convertir a número si es posible
                self.valor = float(self.contenido) if "." in self.contenido else int(self.contenido)
            except ValueError:
                self.valor = self.contenido  # Si no es número, se queda como texto
    
    ## @brief Obtiene el valor como número.
    #  @return Valor numérico de la celda.
    #  @exception ValueError Si el valor no puede convertirse a número.
    def get_numero(self) -> float:
        if self.valor is None:
            return 0
        if isinstance(self.valor, (int, float)):
            return self.valor
        if isinstance(self.valor, str):
            try:
                return float(self.valor) if "." in self.valor else int(self.valor)
            except ValueError:
                raise ValueError(f"No se puede convertir {self.valor} a número")
        raise ValueError("Tipo de valor no soportado")
    
    ## @brief Obtiene el valor como texto.
    #  @return Representación textual del valor.
    def get_texto(self) -> str:
        if self.valor is None:
            return ""
        return str(self.valor)

## @class HojaCalculo
#  @brief Representa la hoja de cálculo completa.
#  @details Almacena celdas y coordina sus actualizaciones.
class HojaCalculo:
    def __init__(self):
        ## @var celdas
        #  @brief Diccionario de celdas, con claves como "A1" y valores Celda.
        self.celdas: Dict[str, Celda] = {}
        ## @var operaciones
        #  @brief Instancia de Operaciones para evaluar fórmulas.
        self.operaciones = Operaciones(self)
    
    ## @brief Obtiene o crea una celda en la coordenada especificada.
    #  @param coord Coordenada de la celda (ej. "A1").
    #  @return Instancia de Celda.
    def get_celda(self, coord: str) -> Celda:
        if coord not in self.celdas:
            self.celdas[coord] = Celda(coord)
        return self.celdas[coord]
    
    ## @brief Establece el contenido de una celda y actualiza dependientes.
    #  @param coord Coordenada de la celda.
    #  @param contenido Nuevo contenido de la celda.
    def set_celda(self, coord: str, contenido: str) -> None:
        celda = self.get_celda(coord)
        celda.set_contenido(contenido, self)
        self._actualizar_dependientes(coord)
    
    ## @brief Actualiza las celdas que dependen de la celda modificada.
    #  @param coord Coordenada de la celda modificada.
    def _actualizar_dependientes(self, coord: str) -> None:
        for celda in self.celdas.values():
            if celda.contenido and celda.contenido.startswith("=") and coord in celda.dependencias:
                celda.actualizar_valor(self)

## @class Operaciones
#  @brief Maneja los cálculos y evaluación de fórmulas.
class Operaciones:
    def __init__(self, hoja: HojaCalculo):
        ## @var hoja
        #  @brief Referencia a la HojaCalculo asociada.
        self.hoja = hoja
    
    ## @brief Evalúa una fórmula y retorna su resultado.
    #  @param formula Texto de la fórmula sin "=".
    #  @param celda Celda donde se evalúa la fórmula.
    #  @return Resultado numérico de la fórmula.
    def evaluar_formula(self, formula: str, celda: Celda) -> float:
        formula = formula.replace(",", ";")  # Convierte separadores de S2V a formato interno
        if formula.startswith("SUMA("):
            return self._evaluar_funcion_suma(formula[5:-1], celda)
        return self._evaluar_expresion(formula, celda)
    
    ## @brief Evalúa la función SUMA.
    #  @param args Argumentos de la función separados por ";".
    #  @param celda Celda actual.
    #  @return Suma de los valores en los argumentos.
    def _evaluar_funcion_suma(self, args: str, celda: Celda) -> float:
        total = 0
        for arg in args.split(";"):
            if ":" in arg:
                inicio, fin = arg.split(":")
                total += self._sumar_rango(inicio, fin)
            else:
                total += self.hoja.get_celda(arg).get_numero()
        return total
    
    ## @brief Suma los valores en un rango de celdas.
    #  @param inicio Coordenada inicial del rango (ej. "A1").
    #  @param fin Coordenada final del rango (ej. "B3").
    #  @return Suma de los valores en el rango.
    def _sumar_rango(self, inicio: str, fin: str) -> float:
        col_inicio = self._col_a_num(inicio)
        col_fin = self._col_a_num(fin)
        fila_inicio = int(re.search(r"\d+", inicio).group())
        fila_fin = int(re.search(r"\d+", fin).group())
        total = 0
        for col in range(col_inicio, col_fin + 1):
            for fila in range(fila_inicio, fila_fin + 1):
                coord = self._num_a_col(col) + str(fila)
                total += self.hoja.get_celda(coord).get_numero()
        return total
    
    ## @brief Convierte una columna (A, AA...) a número.
    #  @param coord Coordenada con columna (ej. "A1").
    #  @return Número entero representando la columna.
    def _col_a_num(self, coord: str) -> int:
        col = re.match(r"[A-Z]+", coord).group()
        return sum((ord(c) - ord("A") + 1) * (26 ** i) for i, c in enumerate(reversed(col)))
    
    ## @brief Convierte un número a notación de columna.
    #  @param num Número entero.
    #  @return String con la notación de columna (ej. "A", "AA").
    def _num_a_col(self, num: int) -> str:
        col = ""
        while num > 0:
            num -= 1
            col = chr(ord("A") + (num % 26)) + col
            num //= 26
        return col
    
    ## @brief Evalúa expresiones aritméticas básicas.
    #  @param expr Expresión a evaluar.
    #  @param celda Celda actual.
    #  @return Resultado numérico.
    def _evaluar_expresion(self, expr: str, celda: Celda) -> float:
        partes = re.split(r"([+-])", expr)
        resultado = 0
        operador = "+"
        for parte in partes:
            parte = parte.strip()
            if parte in {"+", "-"}:
                operador = parte
            elif parte:
                valor = self.hoja.get_celda(parte).get_numero() if re.match(r"[A-Z]+\d+", parte) else float(parte)
                resultado = resultado + valor if operador == "+" else resultado - valor
        return resultado

## @class Interfaz
#  @brief Maneja la interacción con el usuario mediante consola.
class Interfaz:
    def __init__(self, hoja: HojaCalculo):
        ## @var hoja
        #  @brief Referencia a la HojaCalculo asociada.
        self.hoja = hoja
    
    ## @brief Carga un archivo en formato S2V.
    #  @param archivo Ruta del archivo a cargar.
    def cargar_s2v(self, archivo: str) -> None:
        with open(archivo, "r") as f:
            for i, linea in enumerate(f, 1):
                celdas = linea.strip().split(";")
                for j, contenido in enumerate(celdas, 1):
                    if contenido:
                        coord = chr(ord("A") + j - 1) + str(i)
                        self.hoja.set_celda(coord, contenido)
    
    ## @brief Guarda la hoja en formato S2V.
    #  @param archivo Ruta del archivo a guardar.
    #  @param filas Número de filas a guardar.
    #  @param columnas Número de columnas a guardar.
    def guardar_s2v(self, archivo: str, filas: int, columnas: int) -> None:
        with open(archivo, "w") as f:
            for i in range(1, filas + 1):
                linea = []
                for j in range(1, columnas + 1):
                    coord = chr(ord("A") + j - 1) + str(i)
                    celda = self.hoja.get_celda(coord)
                    contenido = celda.contenido if celda.contenido else ""
                    linea.append(contenido.replace(";", ",") if contenido.startswith("=") else contenido)
                f.write(";".join(linea) + "\n")
    
    ## @brief Muestra el menú textual y procesa opciones.
    def menu(self) -> None:
        while True:
            print("\n1. Setear celda\n2. Cargar S2V\n3. Guardar S2V\n4. Salir")
            opcion = input("Seleccione opción: ")
            if opcion == "1":
                coord = input("Coordenada (ej. A1): ")
                valor = input("Valor: ")
                try:
                    self.hoja.set_celda(coord, valor)
                except ValueError as e:
                    print(f"Error: {e}")
            elif opcion == "2":
                archivo = input("Nombre del archivo: ")
                self.cargar_s2v(archivo)
            elif opcion == "3":
                archivo = input("Nombre del archivo: ")
                self.guardar_s2v(archivo, 10, 10)  # Tamaño fijo por simplicidad
            elif opcion == "4":
                break
            else:
                print("Opción inválida")

if __name__ == "__main__":
    hoja = HojaCalculo()
    interfaz = Interfaz(hoja)
    interfaz.menu()