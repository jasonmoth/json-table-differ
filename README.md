This was all ChatGPT.

Useful for comparing SQL results in an application like TablePlus where you can "Copy as JSON"

Place two .JSON files that are arrays of objects

A
```
[
	{
		"ColA": 1,
		"ColB": 2,
		"ColC": 3
	},
	{
		"ColA": 2,
		"ColB": 4,
		"ColC": 6
	}
]
```

B
```
[
	{
		"ColA": 2,
		"ColB": 5,
		"ColC": 6
	}
]
```
Would give the following output

```
JSON files found:
1. Table_A.json
2. Table_B.json

Enter the number of the first file to diff: 1
Enter the number of the second file to diff: 2

Keys in the JSON objects: ['ColA', 'ColB', 'ColC']
Enter the key to use as the unique identifier: ColA

Rows in Table_A.json not in Table_B.json:
1
Rows in Table_B.json not in Table_A.json:

Discrepancies in record 2: ColB
```