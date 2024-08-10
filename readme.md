# About the Learnhelper project

----
Basically i want to document my ways of doing stuff here,
so that others can easily add request to change in my code and we all use the
same way of writing.

We used python 3.12 for the project, so we recommend to install python 3.12+ to work on it.
Be carefull if yu use PyCharm as it uses virtual environments, where you need to set up the 
interpreter in each project properly (factory settings).
You can change the interpreter by going to 

## Licensing
**GNU General Public License (GPL) v3**
1. I allow others to modify my code(Forks or pulls) and create their own versions.
2. Any derived work needs to remain free and open-source. (No adds, no paywalls, no closed source)
3. If you use a mainpart of my code, please let me know, so ive the ability to review and approve modifications before they become public.
4. Using code snippets is all fine, but please mention me in smth. liek credits with a link t this project
(can be in the readme of the github also)
      
## Check this for what to do next:
[TODO](https://github.com/search?q=repo%3Asora7672%2Flearnhelper_api%20%22%23%20TODO%3A%22&type=code)

[FIXME](https://github.com/search?q=repo%3Asora7672%2Flearnhelper_api%20%22%23%20FIXME%3A%22&type=code)
## mysqlmodule
This module used the mysql connector, so you need to install it in your IDE properly.
In PyCharm go to packet manager and search for pip (if you want to install stuff via console)
and then search for "mysql-connector-python" version 9.0.0+.

If you run the MySQL server loacaly you to run there as a root user the
[db_creation_querry.sql]() followed by
[db_example_entry_creation.sql]()

After all this is done, congrats, you have access to my database schema ;)
Go into your mysqlmodule.py and test it to run (with PyCharm it should already work like this)



## Naming of different things with PY and MySQL
### Python
#### Vars
Python accepts in Var/Function names uppercase and numbers.
But no numbers at start and no uppercase at start.
When using *Camelcase* (somethingLikeThat) PyCharm is informing about
wrong standard. So we will use  
***Snakecase*** (looks_like_this_so)
and we DONT want to use numbers in vars

#### Functions / Methods

Here we go similiar as vars, but call them like what they do. 
```python
menu() # Like for showing a menu display
input_numbers() # for showing an input for numbers
get_color() # as Method on a object to grab propertys
set_age() # a method for setting property of an object
update_name() #  a method for updating some values
delete_object() # a method to delete smth. make sure to use delete not del,
# because del is a keyword in python

```
Basically we gve each function/method a clear indicator, what it does.
Except the ones showing (we could call them view tho, but no need so far)

#### Params in Functions/Methods
If we create methods, we could name the parameter like we want.
But we should use a standard, to make files better readable and understandable for all others.
The same goes for names of methods.
```python
def my_function(first_param, second):
    return second - first_param
# not like this!


# pseudo code, imagine in a class that has this attributes
def check_inside(self, x, y):
    if self.x_start <= x <= self.x_end and self.y_start <= y <= self.y_end:
        return True
    else:
        return False
# its ok like this, but the best way you can create your method looks like this:
def check_is_inside(self, position_x: int, position_y: int) -> bool:
    """
    Returns true if the x/y position is inside the objects area.
    Takes as param only integer values
    :param position_x: int
    :param position_y: int
    :return: bool
    """
    if type(position_x) == int and type(position_y) == int:
        if self.x_start <= position_x <= self.x_end and self.y_start <= position_y <= self.y_end:
            return True
        else:
            return False
    else:
        raise ValueError("check_is_inside accepts only ints. Your inputs were (",
                         type(position_x),",",type(position_x), ")")
# thats the best way you could create the method if you work with others.
# docstring, type hinting, input validation and clear var/function naming

```

### MySQL Databases
#### Tables & Procedures & Functions
WIP

#### Columns
WIP


