import user
import functions

filename = functions.request_info()

user1 = user.User.starting_program(filename)

functions.game(user1)




