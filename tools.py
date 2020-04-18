def get_integer_input_for_list(list_length):
    inp = -1
    while inp >= list_length or inp < 0:
        try:
            inp = int(input(f"Which one would you like to edit[0-{list_length-1}]? "))
        except KeyboardInterrupt:
            raise
        except:
            print("Improper input detected. Try again.") 
    return inp

def check_modifier_input(str_in):
    while True:
        try:
            str_in.split(' ')
            if str_in.split(' ')[0] == 'b' and (str_in.split(' ')[1] == 'acc' or str_in.split(' ')[1] == 'uname' or str_in.split(' ')[1] == 'pass' or str_in.split(' ')[1] == 'all'):
                return True 
            else:
                return False
        except:
            print('You missed which entry you want to edit -- [acc, uname, pass, all]')
            return False

        
    
