#Partners: Aileen Ham and Adom-Ahima Amissah
from argparse import ArgumentParser
import re
import sys

LETTER_TO_NUMBER = {
    'A': '2',
    'B': '2',
    'C': '2',
    'D': '3',
    'E': '3',
    'F': '3',
    'G': '4',
    'H': '4',
    'I': '4',
    'J': '5',
    'K': '5',
    'L': '5',
    'M': '6',
    'N': '6',
    'O': '6',
    'P': '7',
    'Q': '7',
    'R': '7',
    'S': '7',
    'T': '8',
    'U': '8',
    'V': '8',
    'W': '9',
    'X': '9',
    'Y': '9',
    'Z': '9'
}

class PhoneNumber:
    """ Takes a phone number and recognizes that it's valid
    
    Attributes:
        area_code (str): the area code 
        exchange_code (str): the exchange code 
        line_number (str): the line number 
        
    """
    def __init__(self, phone_number):
        """ Sets attributes and raises TypeError or ValueError
        
        Args:
            phone_number (str or int): a phone numnber 
            
        Side Effects:
            sets attributes
            
         Raises:
            TypeError: if input is not a string or integer
            ValueError: raised if number is more than 10 digits, 
            area or exchange code starts with '0' or '1' or ends with '11'
        """
        
        self.phone_number = phone_number
        
        if not isinstance(phone_number, (str,int)):
            raise TypeError("Phone number should be a string or integer.")

        phone_number = str(phone_number)
        
        
        convert_letter = (re.sub(r'[A-Z]', lambda match: LETTER_TO_NUMBER.get
                                (match.group(0),''),phone_number))
        phone_number = re.sub(r'\D', '', convert_letter)
        
        if phone_number.startswith('1') and len(phone_number) == 11:
            pass
        elif (len(phone_number) != 10):
            raise ValueError("Phone number is invalid.")
        
        
        expr = r"""(?x)
        (?P<country_code>1\d{0,2})?
        (?P<area_code>\d{3})
        (?P<exchange_code>\d{3})
        (?P<line_number>\d{4})"""
        
        
            
        if re.search(expr,phone_number):
            match = re.search(expr,phone_number)
            
            self.area_code = match.group("area_code")
            if (self.area_code[0] in ('0', '1')) or (self.area_code.endswith('11')):
                raise ValueError("Area code is invalid")
            
            self.exchange_code = match.group("exchange_code")
            if self.exchange_code[0] in ('0', '1') or self.exchange_code.endswith('11'):
                raise ValueError("Exchange code is invalid")
            
            self.line_number = match.group("line_number")
            
    
    def __lt__(self, other):
        """Allows sorting based on the less than operator"""
        self_number = int(f'{self.area_code}{self.exchange_code}{self.line_number}')
        other_number = int(f'{other.area_code}{other.exchange_code}{other.line_number}')
        return self_number < other_number
    
    def __repr__(self):
        """Return a formal representation of the phone number"""
        
        return f"PhoneNumber('{self.area_code}{self.exchange_code}{self.line_number}')"
    
    
    def __str__(self):
        """Return an informal representation of the phone number"""
        return f"({self.area_code}) {self.exchange_code}-{self.line_number}"
    
    def __int__(self):
        """Return integer form of PhoneNumber object."""
        return int(f'{self.area_code}{self.exchange_code}{self.line_number}')
    
    
def read_numbers(filepath):
    """ Reads file and extracts name and phone number 
    
    Args:
        filepath: name of a file 
    
    Returns: 
        list: list of tuples containing names and numbers
    """

    with open(filepath, "r", encoding= "utf-8") as f:
        clean_num = []
        for line in f: 
            info = line.strip().split("\t")
            name = info[0]
            phone_num = info[1]
            try:
                info_tuple = (name, PhoneNumber(phone_num))
                clean_num.append(info_tuple)
            except:
                pass
    sorted_num = sorted(clean_num, key=lambda x: x[1]) 
    return sorted_num
    
def main(path):
    """Read data from path and print results.
    
    Args:
        path (str): path to a text file. Each line in the file should consist of
            a name, a tab character, and a phone number.
    
    Side effects:
        Writes to stdout.
    """
    for name, number in read_numbers(path):
        print(f"{number}\t{name}")

def parse_args(arglist):
    """Parse command-line arguments.
    
    Expects one mandatory command-line argument: a path to a text file where
    each line consists of a name, a tab character, and a phone number.
    
    Args:
        arglist (list of str): a list of command-line arguments to parse.
        
    Returns:
        argparse.Namespace: a namespace object with a file attribute whose value
        is a path to a text file as described above.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file of names and numbers")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
