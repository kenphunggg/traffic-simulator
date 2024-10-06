"""
Generate class based on defined class User
"""
import sys
import os
from lib.ColorfulMessage import Message as Msg

def main(file_name, user_count):
  """
  Generate class
  """

  os.system(f'cp multi_user.py {file_name}.py')

  with open(f'{file_name}.py', 'a', encoding='utf-8') as file:
      for i in range(3, user_count+1):
          class_definition = f'''
class User{i}(User1):
    """Define User to execute AdvanceCurlTask"""
    host = 'http://localhost:2800{i}/mem.php'
    def __init__(self, parent):
        super().__init__(parent)
        self.desire_row = {i}
    '''
          file.write(class_definition)

if __name__ == '__main__':
     # Check if '--help' argument is passed
    if '--help' in sys.argv:
        Msg.YellowMessage('Usage: python3 gen_code.py [name of new file] [total number of users]')
        sys.exit(0)  # Exit after showing help message
    
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        Msg.RedMessage('Error: Wrong syntax')
        Msg.DefaultMessage('Usage: python3 gen_code.py [name of new file] [total number of users]')
        sys.exit(1)  # Exit on error

    try:
        name = sys.argv[1]
        count = int(sys.argv[2])  # Convert the second argument to an integer
    except ValueError:
        Msg.RedMessage('Error: [total number of users] should be an integer.')
        sys.exit(1)

    # Call the main function with the valid arguments
    main(name, count)
