# NOTES.md — Week 2: Config-Driven Data Pipelines

**Student ID used with `generate_for_student.py`:**
<!-- paste the --student-id value you used -->
112301031  


## What was hardcoded, and what would switching it have required?  

<!-- What specifically was hardcoded in the original script, and what would
     have had to happen to change the threshold or switch formats before
     your refactor? -->  
What specifically was hardcoded in the original script?  
- VARIABLES: INPUT_PATH, HIGH_VALUE_THRESHOLD, OUTPUT_PATH  
- Assumed the input file's format to always be csv  

What would have had to happen to change the threshold or switch formats before your refactor?   
- To change threshold we have to change the file variable HIGH_VALUE_THRESHOLD and redeploy it (which is not very good exactly)  
- A json file which it should support will make it to be improperly read.
(Though we may need to have seperate loading functions for seperate fmts)
