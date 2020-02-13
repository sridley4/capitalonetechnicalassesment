import sys
import re
from collections import Counter

SLASH_COMMENTS_REGEX = re.compile('(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)')
HASH_TAG_COMMENTS_REGEX = re.compile('(?:#\\*(?:[^*]|(?:\\*+[^*#]))*)|(?:#.*)')
TODO_REGEX = re.compile('(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.TODO.*)|(?:#\\*(?:[^*]|(?:\\*+[^*#]))*\\*+/)|(?:#*TODO.*)|(?:\\*.TODO.*)')
SLASH_BLOCK_COMMENT_REGEX = re.compile('(?:/\\*)|(?:\\*)|(?:\\/\\*)')
END_SLASH_BLOCK_COMMENT_REGEX = re.compile('(?:\\*\\/)')
FILE_EXTENSION_REGEX = re.compile('([a-zA-Z0-9\s_\\.\-\(\):])+(\..*[a-zA-Z])$')




def count_comments(fileLines):
    myMap = Counter({"total_lines": 0, "commented_lines": 0, "single_commented_lines": 0, "comments_within_block_comments": 0, "block_comments": 0, "todos_comments": 0}) 

    myFlags = dict({"hash_tag_comment_flag": False, "slash_block_comment": False, "hash_tag_comment_block_flag": False})

    for x in fileLines:
        myMap.update({'total_lines':1})
        if(SLASH_COMMENTS_REGEX.search(x) or HASH_TAG_COMMENTS_REGEX.search(x) or SLASH_BLOCK_COMMENT_REGEX.search(x)):
            identify_comment(x, myMap, myFlags)
        else:
            check_flags(myFlags)
    
    return myMap
        
    

def identify_comment(x, myMap, myFlags):
    myMap.update({'commented_lines':1})

    if(HASH_TAG_COMMENTS_REGEX.search(x)):
        identify_hash_tag_comment(myMap, myFlags)
    elif(SLASH_BLOCK_COMMENT_REGEX.search(x) or myFlags.get("slash_block_comment")):
        identify_slash_block_comment(x, myMap, myFlags)
    else:
        myMap.update({"single_commented_lines",1})

    if(TODO_REGEX.search(x)):
        myMap.update({'todos_comments':1})

def check_flags(myFlags):
    if(myFlags.get("hash_tag_comment_block_flag")):
        myFlags["hash_tag_comment_block_flag"] = False
        myFlags["hash_tag_comment_flag"] = False
    elif(myFlags.get("hash_tag_comment_flag")):
        myFlags["hash_tag_comment_flag"] = False

def identify_hash_tag_comment(myMap, myFlags):
    if(myFlags.get('hash_tag_comment_block_flag')):
        myMap.update({"comments_within_block_comments",1})
    elif(myFlags.get('hash_tag_comment_flag')):
        myFlags['hash_tag_comment_block_flag'] = True
        myMap["comments_within_block_comments"] += 2
        myMap.subtract({"single_commented_lines"})
        myMap.update({"block_comments",1})
    else:
        myFlags['hash_tag_comment_flag'] = True
        myMap.update({"single_commented_lines",1})

def identify_slash_block_comment(x, myMap, myFlags):
    if(END_SLASH_BLOCK_COMMENT_REGEX.search(x)):
        myFlags['slash_block_comment'] = False
        myMap.update({"comments_within_block_comments",1})
    else:
        if(myFlags.get("slash_block_comment")):
            myMap.update({"comments_within_block_comments",1})
        else:
            myMap.update({"comments_within_block_comments",1})
            myMap.update({"block_comments",1})
            myFlags['slash_block_comment'] = True

if __name__ == "__main__":  
    print("Name of script is ", sys.argv[0])
    print("Reading file ", sys.argv[1])
    if not FILE_EXTENSION_REGEX.search(sys.argv[1]):
        print("File can be ignored as it doesn't follow proper naming conventions.")
        sys.exit()
    fl = open(sys.argv[1], "r+")
    fileLines = fl.readlines()
    
    myMap = count_comments(fileLines)
    print("Total number of lines: " + str(myMap.get('total_lines')))
    print("Total number of comments: " + str(myMap.get('commented_lines')))
    print("Total number of single commented lines: " + str(myMap.get('single_commented_lines')))
    print("Total number of comments in blocks: " + str(myMap.get('comments_within_block_comments')))
    print("Total number of blocks: " + str(myMap.get('block_comments')))
    print("Total number of TODOs: " + str(myMap.get('todos_comments')))
