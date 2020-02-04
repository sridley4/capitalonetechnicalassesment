import sys
import re
from collections import Counter

hash_tag_comment_flag = False


slash_comments = re.compile('(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)')
hash_tag_comment = re.compile('(?:#\\*(?:[^*]|(?:\\*+[^*#]))*\\*+/)|(?:#.*)')
todo = re.compile('(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.TODO.*)|(?:#\\*(?:[^*]|(?:\\*+[^*#]))*\\*+/)|(?:#*TODO.*)|(?:\\*.TODO.*)')
slash_block_comment = re.compile('(?:/\\*)|(?:\\*)|(?:\\/\\*)')
end_slash_block_comment = re.compile('(?:\\/\\*)')
file_extension = re.compile('([a-zA-Z0-9\s_\\.\-\(\):])+(\..[a-zA-Z0-9])$')


myMap = Counter({"total_lines": 0, "commented_lines": 0, "single_commented_lines": 0, "comments_within_block_comments": 0, "block_comments": 0, "todos_comments": 0}) 

myFlags = dict({"hash_tag_comment_flag": False, "slash_block_comment": False, "hash_tag_comment_block_flag": False})

def count_comments():
    print("Name of script is ", sys.argv[0])
    print("Reading file ", sys.argv[1])
    if not file_extension.search(sys.argv[1]):
        print("File can be ignored as it doesn't follow proper naming conventions.")
        return
    fl = open(sys.argv[1], "r+")
    fileLines = fl.readlines()

    for x in fileLines:
        myMap.update({'total_lines':1})
        if(slash_comments.search(x) or hash_tag_comment.search(x) or slash_block_comment.search(x)):
            identify_comment(x)
        elif(myFlags.get("hash_tag_comment_block_flag")):
            myFlags["hash_tag_comment_block_flag"] = False
            myFlags["hash_tag_comment_flag"] = False
        elif(myFlags.get("hash_tag_comment_flag")):
            myFlags["hash_tag_comment_flag"] = False
    
    print("Total number of lines: " + str(myMap.get('total_lines')))
    print("Total number of comments: " + str(myMap.get('commented_lines')))
    print("Total number of single commented lines: " + str(myMap.get('single_commented_lines')))
    print("Total number of comments in blocks: " + str(myMap.get('comments_within_block_comments')))
    print("Total number of blocks: " + str(myMap.get('block_comments')))
    print("Total number of TODOs: " + str(myMap.get('todos_comments')))
    

def identify_comment(x):
    myMap.update({'commented_lines':1})

    if(hash_tag_comment.search(x)):
        if(myFlags.get('hash_tag_comment_block_flag')):
            myMap.update({"comments_within_block_comments",1})
        elif(myFlags.get('hash_tag_comment_flag')):
            myFlags['hash_tag_comment_block_flag'] = True
            myMap.update({"comments_within_block_comments",1})
            myMap.update({"comments_within_block_comments",1})
            myMap.subtract({"single_commented_lines"})
            myMap.update({"block_comments",1})
        else:
            myFlags['hash_tag_comment_flag'] = True
            myMap.update({"single_commented_lines",1})

    elif(slash_block_comment.search(x)):
        if(end_slash_block_comment.search(x)):
            myFlags['slash_block_comment'] = False
            myMap.update({"comments_within_block_comments",1})
        else:
            if(myFlags.get("slash_block_comment")):
                myMap.update({"comments_within_block_comments",1})
            else:
                myMap.update({"comments_within_block_comments",1})
                myMap.update({"block_comments",1})
                myFlags['slash_block_comment'] = True
    else:
        myMap.update({"single_commented_lines",1})

    if(todo.search(x)):
        myMap.update({'todos_comments':1})

count_comments()



