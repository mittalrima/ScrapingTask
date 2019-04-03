This is a sample scraping project that scrapes University of Chicago course pages to get the course information. 
This uses a custom queue implementation to scrape subpages in a parent page.

# Scraping Test

Steps to run :

# Clone the project from github
1. Clone the project

# Create a virtual env
2. virtualenv venv

# Enter the virtual Environment
3. source venv/bin/activate

# Run a clean build - this will remove any existing target folders.
4. pip install pybuilder
5. pyb clean

## Run a build
6. pyb

## Install the dependencies
7. pyb install

## Test
Run the test script at src/main/python/scrapingTask.py. The results get saved in the variable variable links_crawled. 
It is a nested list of dictionary. It can be interpreted as JSON and further used.




The result is a JSON Array, one sample element of the JSON Array looks like:

{
'link': 'http://www.classes.cs.uchicago.edu/archive/2015/winter/12200-1/new.collegecatalog.uchicago.edu/thecollege/history/index.html',
'Courses': [
{
'course_title': 'HIST\xa010101-10102.  Introduction to African Civilization I-II.',
'course_desc': '\nCompletion of the general education requirement in social sciences recommended. Taking these courses in sequence is recommended but not required. This sequence meets the general education requirement in civilization studies. African Civilization introduces students to African history and cultures in a two-quarter sequence.',
'sub_course': [
  {
    'course_title': 'HIST\xa010101.  Introduction to African Civilization I.  100 Units.',
    'course_desc': '\nPart one considers literary, oral, and archeological sources to investigate African societies and states from the early Iron Age through the emergence of the Atlantic world. Case studies include the empires of Ghana, Mali, and Great Zimbabwe. The course also treats the diffusion of Islam, the origins and effects of European contact, and the trans-Atlantic slave trade.'
  },
  {
    'course_title': 'HIST\xa010102.  Introduction to African Civilization II.  100 Units.',
    'course_desc': '\nPart two takes a more anthropological focus, concentrating on Eastern and Southern Africa, including Madagascar. We explore various aspects of colonial and postcolonial society. Topics covered include the institution of colonial rule, ethnicity and interethnic violence, ritual and the body, love, marriage, money, youth and popular culture.'
  }
]
}


