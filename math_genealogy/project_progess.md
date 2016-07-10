### Progress on data science project as of 10/7/2016

My current plan for my project is to look at the data available about mathematicians and their student/advisor relationships from the math genealogy project:
http://www.genealogy.ams.org/index.php

I have started by writing a script to scrape the math genealogy website. Each mathematician gets their own id, and their pages differ only by this id so it makes it easy to connect and download each webpage. However, there are a couple of problems with my script because not all the pages a formatted in exactly the same way. However, I did manage to scrape about 60000 webpages.

I ran some simple analysis on the first 17000 pages by plotting number of students and number of descendants against the year the mathematician completed their thesis. This reveal some expected trends, for example, mathematicians that have recently completed their thesis tend not to have many students.

Some of my data is malformed because of varied webpage layout. For example, sometimes the year field became populated by a string. Also, sometimes my script wasn't able to pull out the correct number of students or descendants of a given mathematician. Also, while I was able to scrape the first 60000 pages, the files containing entries past 17000 seem to be corrupted, or at least pandas is not able to read them.

I have a couple of directions that the project could go in:
1. I am interested in the evolution of thesis topic (represented as key words in thesis title) with time (ie year of thesis completion)
2. Linking the genealogy data with paper citations. We could look for authors with few students but an advisor with alot of students, suggesting popularity of a paper due to their advisor.
