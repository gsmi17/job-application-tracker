# AI Usage Documentation

## Tools Used
- Claude — primary tool for generating Flask routes, and SQL schema
- ChatGPT - help with errors in code, helped with making stylesheet more colorful and modern


## Key Prompts

1. "Help me build a Flask route CRUD for 4 tables: companies, jobs, applications, contacts. Include a Job Match feature where users enter skills and see ranked results."

2. "Help me write a MySQL schema for the 4 tables, the one I have is giving me errors"

3. "Create a Flask route that takes user skills, queries all jobs with JSON requirements, and returns them sorted by match percentage"

4. "Help me edit my stylesheet to create a more colorful but modern look"

5. "My program keeps just showing a blank page but I don't think there is a problem with my code, what else could be causing the issue?"


## What Worked Well

- Claude generated the full CRUD route structure very quickly, the pattern is repetitive across all 4 tables.
- The Job Match percentage algorithm came out correctly on the first try.
- AI was able to help me with creation and debugging of Python code.
- Helped me rewrite my MySQL schema after it kept giving me errors. 
- Help me solve issues like my program showing just a blank page instead of my project.


## What I Modified

- Changed the `get_db()` function to accept my actual MySQL credentials
- Fixed some the JSON parsing 
- Renamed CSS classes to be more descriptive
- Added flash messages for CRUD operations
- Added extra symbols and details in base to change the style of the side bar


## Lessons Learned

1. Always test AI code immediately, it often has small bugs.
2. Ask for explanations, not just code, asking "explain why" after getting code helped me understand, especilly as I'm new
at using Python.
3. AI doesn't know your environmenthad to adjust things like the MySQL connector setup for my specific project
4. Pasting error messages back into the chat to debug was very efficient

