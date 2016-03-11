import sys

class SimpleDB:

    def __init__(self):
        # Use stack_history as a Stack, so that I can store my old database
        self.stack_history = []
        # Current database
        self.database = dict()

    def get(self, name):
        # if key exists: print value, otherwise: print NULL
        if name in self.database:
            print(self.database[name])
        else:
            print("NULL")

    def set(self, name, value):
        if len(self.stack_history) > 0:
            # Move the old value in the stack_history, so that I can rollback
            if name in self.database and name not in self.stack_history[0]:
                self.stack_history[0][name] = self.database[name]
            # name was not in the database, so I write None in the stack_history so that I can rollback
            if name not in self.database:
                self.stack_history[0][name] = None
        # Write into the database the name and the value
        self.write(name, value)


    def end(self):
        # Exit the program
        sys.exit()

    def unset(self, name):
        # set None to the database for the key name, and move the old value to the stack_history
        if name in self.database:
            self.set(name, None)

    def num_equal_to(self, value):
        # print the number of value equal to value in the database
        resu = 0
        for key, value_db in self.database.items():
            if value == value_db:
                resu += 1
        print(resu)


    def commit(self):
        # Empty the stack (Close all open transaction blocks) or print NO TRANSACTION
        if len(self.stack_history) > 0:
            self.stack_history = []
        else:
            print("NO TRANSACTION")

    def begin(self):
        # Create a new dict on the Stack
        self.stack_history.insert(0, dict())

    def rollback(self):
        # Move the value of the Stack (old) to the Database
        if len(self.stack_history) > 0:
            for key, value in self.stack_history[0].items():
                self.write(key, value)
            self.stack_history.pop(0)
        else:
            print("NO TRANSACTION")

    def write(self, name, value):
        # Write the value to the database
        if value != None:
            self.database[name] = value
        # Delete the value if UNSET
        else:
            del self.database[name]


    def command_valid(self, args):
        # Try: if user try to access a 'index out of range' argument
        try:
            # Check for all methods if it has the right command, and the right number of arguments
            if args[0] == "END" and len(args) == 1:
                self.end()
            elif args[0] == "SET" and len(args) == 3:
                self.set(args[1], args[2])
            elif args[0] == "GET" and len(args) == 2:
                self.get(args[1])
            elif args[0] == "UNSET" and len(args) == 2:
                self.unset(args[1])
            elif args[0] == "NUMEQUALTO" and len(args) == 2:
                self.num_equal_to(args[1])
            elif args[0] == "COMMIT" and len(args) == 1:
                self.commit()
            elif args[0] == "BEGIN" and len(args) == 1:
                self.begin()
            elif args[0] == "ROLLBACK" and len(args) == 1:
                self.rollback()
            else:
                print("Bad arguments")
        except IndexError as detail:
            print("Bad arguments: ",detail)

    def run(self):
        # Main loop
        while True:
            # Take input
            args = input().split()
            # Check arguments
            self.command_valid(args)

if __name__ == '__main__':
    simpleDB = SimpleDB()
    simpleDB.run()