# -*- coding: utf-8 -*-
"""
This will just run al the code we want to run
it will be splited into different modules,
to have a better overview about stuff
"""




def start_app():
    print("Hello world")
    pass




# # # # # CODE TO RUN # # # # #


if __name__ == "__main__":
    start_app()



text =  "What will be the output of the following code?\n\n```python\nprint(type([]) is list)\n```"

max = 20
codeblock = "```python\nprint(type([]) is list)\n```"
out= ["What will be the","output of the", "following code?", "\n", "{codeblock}"]

out = ["What will be the","output of the", "following code?", "\n", "```python\nprint(type([]) is list)\n```"]