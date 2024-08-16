/* This procedures should create now entrys for testing*/
CALL `learnhelper`.`add_test_type`("Python All", NULL);
CALL `learnhelper`.`add_test_type`("SQL All", NULL);
CALL `learnhelper`.`add_test_type`("NoSQL All", NULL);
CALL `learnhelper`.`add_test_type`("Project Management All", NULL);

CALL `learnhelper`.`add_person`("Admin","mail@test.de", "aFakeHash");
CALL `learnhelper`.`add_person`("Test User","mail@test.de","aFakeHash");
CALL `learnhelper`.`add_person`("Dozent","mail@test.de","aFakeHash"");

/*  This should add the parents correct if you use this on an empty database & tables */
CALL `learnhelper`.`add_question`(
    "What is the output of the following Python code?\n\n```python\nprint('Hello, World!')\n```",
    1,
    True,
    "Hello, World!",
    "Hello World!",
    "hello, world!",
    "Syntax Error",
    True,
    False,
    False,
    False
);

CALL `learnhelper`.`add_question`(
    "What is the output of the following Python code?\n\n```python\nprint('Hello, World!')\n```",
    1,
    True,
    "Hello, World!",
    "Hello World!",
    "hello, world!",
    "Syntax Error",
    True,
    False,
    False,
    False
);

CALL `learnhelper`.`add_question`(
    "Which of the following are valid ways to create a list in Python?",
    1,
    False,
    "list1 = [1, 2, 3]",
    "list2 = list([1, 2, 3])",
    "list3 = list(1, 2, 3)",
    "list4 = [1, 2, 3,]",
    True,
    True,
    False,
    True
);

CALL `learnhelper`.`add_question`(
    "What is the output of the following code?\n\n```python\nx = [1, 2, 3]\nprint(x[1])\n```",
    1,
    True,
    "1",
    "2",
    "3",
    "IndexError",
    False,
    True,
    False,
    False
);

CALL `learnhelper`.`add_question`(
    "Which of the following statements are true about Python dictionaries?",
    1,
    False,
    "They are unordered collections.",
    "They are mutable.",
    "Keys must be unique.",
    "Values must be unique.",
    True,
    True,
    True,
    False
);

CALL `learnhelper`.`add_question`(
    "What will be the output of the following code?\n\n```python\nfor i in range(3):\n    print(i)\n```",
    1,
    True,
    "0 1 2",
    "0 1 2 3",
    "1 2 3",
    "None of the above",
    True,
    False,
    False,
    False
);

CALL `learnhelper`.`add_question`(
    "Which of the following are valid Python variable names?",
    1,
    False,
    "variable_1",
    "1_variable",
    "_variable",
    "variable-1",
    True,
    False,
    True,
    False
);

CALL `learnhelper`.`add_question`(
    "What will be the output of the following code?\n\n```python\nprint(type([]) is list)\n```",
    1,
    True,
    "True",
    "False",
    "TypeError",
    "None of the above",
    True,
    False,
    False,
    False
);

CALL `learnhelper`.`add_question`(
    "Which of the following methods can be used to add an element to a list in Python?",
    1,
    False,
    "append()",
    "add()",
    "insert()",
    "extend()",
    True,
    False,
    True,
    True
);

CALL `learnhelper`.`add_question`(
    "What will be the output of the following code?\n\n```python\nx = [1, 2, 3]\nprint(len(x))\n```",
    1,
    True,
    "2",
    "3",
    "4",
    "TypeError",
    False,
    True,
    False,
    False
);

CALL `learnhelper`.`add_question`(
    "Which of the following are correct ways to create a set in Python?",
    1,
    False,
    "set1 = {1, 2, 3}",
    "set2 = set([1, 2, 3])",
    "set3 = {1, 2, 3, 3}",
    "set4 = set(1, 2, 3)",
    True,
    True,
    True,
    False
);

CALL learnhelper.add_question(
    'What is the output of the following Python code: ''print(sum([1, 2, 3, 4, 5]))''?',
    1,
    TRUE,
    '6',
    '5',
    '4',
    '3',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''yield'' keyword in Python?',
    1,
    TRUE,
    'To return a value from a function',
    'To pause the execution of a function',
    'To pass a value to a function',
    'To resume the execution of a function',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the difference between ''break'' and ''continue'' statements in Python?',
    1,
    TRUE,
    'Break stops the execution of a loop, while continue skips to the next iteration',
    'Break skips to the next iteration, while continue stops the execution of a loop',
    'Break and continue are used to exit a loop',
    'Break and continue are used to pause a loop',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''enumerate'' function in Python?',
    1,
    TRUE,
    'To iterate over a list of numbers',
    'To iterate over a list of strings',
    'To iterate over a list of tuples',
    'To iterate over a list of indices and values',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the output of the following Python code: ''print([x**2 for x in range(5)])''?',
    1,
    TRUE,
    '[0, 1, 4, 9, 16]',
    '[1, 4, 9, 16, 25]',
    '[0, 1, 4, 9, 25]',
    '[1, 4, 9, 16, 25]',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''lambda'' function in Python?',
    1,
    TRUE,
    'To define a function with a single expression',
    'To define a function with multiple expressions',
    'To define a function with no arguments',
    'To define a function with a single argument',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);


CALL learnhelper.add_question(
    'What is the output of the following Python code: ''print(reversed([1, 2, 3, 4, 5]))''?',
    1,
    TRUE,
    '[5, 4, 3, 2, 1]',
    '[1, 2, 3, 4, 5]',
    '[5, 4, 3, 2, 1, 0]',
    '[5, 4, 3, 2, 1, 0]',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''zip'' function in Python?',
    1,
    TRUE,
    'To concatenate two lists',
    'To iterate over two lists simultaneously',
    'To merge two lists into one',
    'To split a list into two lists',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the output of the following Python code: ''print(set([1, 2, 2, 3, 4, 4, 5]))''?',
    1,
    TRUE,
    '{1, 2, 3, 4, 5}',
    '{1, 2, 3}',
    '{1, 2, 3, 4}',
    '{1, 2, 3, 4, 5}',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''sorted'' function in Python?',
    1,
    TRUE,
    'To sort a list in descending order',
    'To sort a list in ascending order',
    'To sort a list in random order',
    'To sort a list in reverse order',
    TRUE,
    FALSE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''INDEX'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To create an index on a column',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''SELECT'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To retrieve data from a table',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''JOIN'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To combine data from two tables',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''GROUP BY'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To group data by one or more columns',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''HAVING'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To filter grouped data',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''LIMIT'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To limit the number of rows returned',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''ORDER BY'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To sort data in ascending or descending order',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''SUBQUERY'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To use the result of a query as an argument for another query',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''TRIGGER'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To execute a set of statements in response to a specific event',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

CALL learnhelper.add_question(
    'What is the purpose of the ''VIEW'' command in MySQL?',
    2,
    FALSE,
    'To create a table',
    'To insert data into a table',
    'To create a virtual table based on the result of a query',
    'To delete a table',
    FALSE,
    TRUE,
    FALSE,
    FALSE
);

UPDATE `questions`
SET `validated_for_tests` = 1
WHERE `id` != 0;