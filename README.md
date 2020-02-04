# capitalonetechnicalassesment
I used regex to identify comments and kept track of block statements using flags. I figured the most efficient way to count the comments would be while reading through the file line by line. Regex does take O(n) time however. My script could be made to be more efficient by separating the block regex and slash regex to separate functions that would be called depending on the file extension of what is being passed in.

To run enter:
<code>python comment_counter.py 'filePassedIn'</code>
