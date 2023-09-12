import yaml
import datetime
import tiktoken

def readYaml(file_path):
    ''' Reads a YAML file and returns its contents as a dictionary in Python. '''
    with open(file_path, "r", encoding='utf-8') as f:
        return yaml.safe_load(f)


def getMessageTime():
    ''' Returns the current date and time in specific format, including the day of the week in Spanish. '''
    daysOfWeek =["lunes", "martes", "miércoles","jueves", "viernes", "sábado", "domingo"]
    now = datetime.datetime.now()
    return now.strftime(daysOfWeek[now.weekday()] + ' %d/%m/%Y y son las %H:%M')  


def getNumTokens(string, encodingName):
    ''' Returns the number of tokens in a text string. '''
    encoding = tiktoken.get_encoding(encodingName)
    numTokens = len(encoding.encode(string))
    return numTokens
