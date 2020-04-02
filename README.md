# GraphT-Project

# Introduction
This is a software development Year 3 project for graph theory  
It is a program to execute regular expressions on strings using  
an algorithm known as Thompson’s construction. The project is  
written in python language and the version used is python3. The  
shunting algorithim is used which uses the Thompson's construction

# How to Run
git clone https://github.com/MateuszPawlowski/GraphT-Project  
cd GraphT-Project  
python3 project.py

# Examples Used
**Tests for '.', '|', '*'**  
"a.b|b*", "bbbbb", True  
"a.b|b*", "bbbbx", False  
"b**", "b", True  
"b*", "", True  
    
**Tests for '?'**  
"a?", "", True  
"a?", "a", True  
"a?b|b*", "bbb", True  
"a?b", "a",False  
"a?b", "b", True  

**Tets for '+'**  
"a+", "", False  
"a+", "a", True  
"a+b|b", "bbb", True  
"a+b|b*", "a", False  
"a+|b", "a", True  
"a+|b", "", False

# Resources
**Official Python Website**  
https://www.python.org/  

**GeeksforGeeks' list of graph algorithms.**  
https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/  
