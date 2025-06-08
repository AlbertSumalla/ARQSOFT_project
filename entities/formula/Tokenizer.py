from typing import List

class Tokenizer:
    @staticmethod
    def tokenize(formula_str: str) -> List[str]:
        tokens: List[str] = []
        current_token = ""

        for char in formula_str:
            # Si es espacio, finalizamos el token actual
            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                continue

            # Si es letra o dígito o punto, lo añadimos al token en construcción
            if char.isalnum() or char == '.':
                current_token += char
            else:
                # Primero añadimos el token anterior si existe
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                # Luego añadimos el carácter actual como token separado
                tokens.append(char)

        # Añadimos el último token si quedó algo
        if current_token:
            tokens.append(current_token)

        return tokens