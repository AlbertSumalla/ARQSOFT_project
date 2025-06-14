import re
from typing import List

class Tokenizer:
    # Order matters: longer patterns first
    _TOKEN_RE = re.compile(
        r'\d+\.\d+|'           # decimal numbers
        r'\d+|'                # integer numbers
        r'[A-Za-z]+[0-9]+|'    # cell references, e.g. A1, AB12
        r'[A-Za-z_]\w*(?=\()|' # function names (letters+digits) before '('
        r'[A-Za-z_]\w*|'       # standalone words (if you ever support named constants)
        r'[+\-*/^();:]'        # operators and punctuation
    )

    @staticmethod
    def tokenize(formula_str: str) -> List[str]:
        """
        Split a formula (without the leading '=') into tokens.
        
        Recognizes:
          - decimal numbers: 123.45
          - integers: 678
          - cell refs: A1, BC23
          - function names: SUM, MyFunc (when followed by '(')
          - operators: + - * / ^ 
          - punctuation: ( ) , :
        
        Example:
          tokenize('SUM(A1:B3, 5+X2)') 
            -> ['SUM','(','A1',':','B3',',','5','+','X2',')']
        """
        return Tokenizer._TOKEN_RE.findall(formula_str) # findall will automatically drop whitespace etc.