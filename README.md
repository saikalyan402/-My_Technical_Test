# python-etl
A library which works on a config json to read from the source file apply the transformation and pushes the transformed result into sink.

## Pre-requisite
- Install python@3.7 or above versions
- Run `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`

## How to run this utility
Before actually running this utility we need to understand the config json based on which it is going to run.

- config.json
  Below is a sample config.json file
  ```json
  {
    "reader": {
        "connector": {
            "type": "file",
            "config": {
                "path": "/path/to/input/file/input.txt"
            }
        }
    },
    "transform": [
        {
            "type": "TO_UPPER"
        }
    ],
    "writer": {
        "connector": {
            "type": "file",
            "config": {
                "path": "/path/to/inpur/directory/"
            }
        }
    }
  }
  ```
  **Reader Configurations:**
   - you can create reader config like below. The most important part is the connector
    ```json
        "reader": {
            "connector": {
                "type": "file",
                "config": {
                    "path": "path/to/your/file"
                }
            }
        }
    ```
  - Data Connector help connect to external sources on which transformations can be applied.
  - List of supported data connectors and future scope:
    - file
    - jdbc (future scope)
    - any custom connector (can be added in future)
  - **Connector Key Parameters:**

    | Name    | Type     | Description                            | Supported Values                                 |
    |:--------|:---------|:---------------------------------------|:-------------------------------------------------|
    | type    | `String` | Type of the Connector                  | file, kdbc, custom |
    | config  | `Object` | Configuration params of the connector  | Depends on connector type (see below)            |

    #### For File based Data Connectors:
     - **config** object supports the following keys,

        | Name       | Type     |Description                            | Supported Values | Default Values |
        |:-----------|:---------|:---------------------------------------|:-----------------|:-------------- |
        | path      |`String`   | path(s) to be read | | `Empty` |
    
    #### For jdbc based Data Connectors (future scope):
    - **config** object supports the following keys,

        | Name       | Type     | Description                            | Default Values |
        |:-----------|:---------|:---------------------------------------|:-------------- |
        | database   | `String` | database name                          | default |
        | tablename  | `String` | table name to be read                  | `Empty` |
        | url        | `String` | the connection string URL to database  | `Empty` |
        | user       | `String` | user for connection to database        | `Empty` |
        | password   | `String` | password for connection to database    | `null`  |
        | driver     | `String` | driver class for JDBC connection to database | com.mysql.jdbc.Driver |
        | where      | `String` | condition for reading data from table  | `Empty` |

  **Writer Configurations:**
    
    This configuration is same as reader configuration.

  **Transform Configurations:**
    
    We can have list of transformations defined. It can be created like below. I have kept list of transformations for future scope. Though it currently works if you provide miltiple transformations. Where it will write the output for multiple transformations into multiple files.
    ```json
        "transform": [
            {
                "type": "TO_UPPER"
            }
        ]
    ```
    - Currently supported transform types:
        - TO_UPPER  (convert every letter in the text into upper case)
        - UNIQUE_WORD_COUNT (counts each unique words)

**Now we will look into how to run this utility**
```bash
cd <BASE_PROJECT_LOCATION>/pythonetl
#prepare the config.json file based on configuration guide I provided in the above section
#you can understand the runner arguments
python3 runner.py --help
# bash-3.2$ python3 runner.py --help
# usage: runner.py [-h] --config_json path

# Takes config json as input and runs this utility

# optional arguments:
#   -h, --help          show this help message and exit
#   --config_json path  the path to config json file

python3 runner.py --config_json ../tests/config.json

# bash-3.2$ python3 runner.py --config_json ../tests/config.json 
# ../tests/config.json
# initializing the file data connector
# printing the present config {'path': '../tests/input.txt'}
# initializing the sink file data connector
# printing the present config {'path': '../tests'}
# [ToUpperTransformation(type='TO_UPPER')]
# writing data into this path: ../tests/TO_UPPER1667634559ff4a9d9f8a1d5926cd21d4.txt
```


  


