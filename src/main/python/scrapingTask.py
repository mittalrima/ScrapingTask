from src.main.python.CustomQueue import MyQueue
from src.main.python import constants
from src.main.python.utiloriginal import *

# The list(of dictionaries containing information about the links traversed and the courses found.)
links_crawled = []

# The queue used for maintaining the crawling order
links_queue = MyQueue()

# counter to maintain the number of pages crawled
pages_crawled = 0


# function to check if its okay to scrape the URL.
def check_ok_to_scrape(url):
    '''
    :param url: the url
    :return: boolean value true if the URL is okay for scraping.
    '''
    if is_url_in_dict_list(url):
        return False
    if not is_url_ok_to_follow(url, constants.LIMITING_DOMAIN):
        return False
    return True


def is_url_in_dict_list(url):
    '''

    :param url: the url
    :return: true if the url is in the dictionary list and has been crawled already
    '''
    if not any(d.get('link', None) == url for d in links_crawled):
        return False
    return True


def get_url_to_scrape(parent_url, url):
    '''
    This method takes a URL and converts it, also checks for fragments.
    :param parent_url: the main page url being crawled
    :param url: the url from the href tag
    :return: the converted url. Returns None if the URL is not okay to scrape.
    '''
    if not is_absolute_url(url):
        url = convert_if_relative_url(parent_url, url)
    if not check_ok_to_scrape(url):
        return None
    url = remove_fragment(url)
    return url


def add_to_crawled_list(url, courses):
    '''
    This method updates the result list with all the information after scraping
    :param url: the url scraped
    :param courses: the course dictionary object
    :return: void
    '''
    link_map = dict([
        ("link", url),
        ("Courses", courses)
    ])
    links_crawled.append(link_map)
    return


def add_url_to_queue(parent_url, url):
    '''
    This method adds the converted url to the queue for processing
    :param parent_url: the parent url
    :param url: the url from href anchor tags
    :return: void
    '''
    url = get_url_to_scrape(parent_url, url)
    if url is not None:
        links_queue.enqueue(url)


def scrape_from_queue():
    '''
    This method pops an element from the queue and reads the response
    :return: void
    '''
    content = ""
    url_to_scrape = links_queue.dequeue()
    print(url_to_scrape)
    response = get_request(url_to_scrape)
    global pages_crawled
    pages_crawled = pages_crawled + 1
    if response is not None:
        content = read_request(response)
    parse_content(url_to_scrape, content)


def parse_content(url, content):
    '''
    This method parses the html read.
    :param url: the url
    :param content: the html content
    :return: void
    '''
    soup = bs4.BeautifulSoup(content, "html5lib")
    course_main_divs = soup.find_all('div', class_="courseblock main")
    courses = []
    # reading all course_main divs
    for course_main in course_main_divs:
        title = course_main.find('p', class_="courseblocktitle").text
        desc = course_main.find('p', class_="courseblockdesc").text
        sub_courses = []
        # reading all subsequences
        next_sub_sequence = course_main.find_next_sibling('div')
        while next_sub_sequence and next_sub_sequence['class'] == ['courseblock', 'subsequence']:
            sub_title = next_sub_sequence.find('p', class_="courseblocktitle").text
            sub_desc = next_sub_sequence.find('p', class_="courseblockdesc").text
            sub_course = dict([
                ("course_title", sub_title),
                ("course_desc", sub_desc)
            ])
            sub_courses.append(sub_course)
            next_sub_sequence = next_sub_sequence.find_next_sibling('div')
        course = dict([
            ("course_title", title),
            ("course_desc", desc),
            ("sub_course", sub_courses)
        ])
        courses.append(course)
    add_to_crawled_list(url, courses)
    # adding all new links to queue
    for anchor in soup.find_all('a'):
        if anchor.has_attr('href'):
            add_url_to_queue(url, anchor['href'])


def start_crawling():
    '''
    The method where crawling starts. This prints the final result list.
    :return: void
    '''
    add_url_to_queue("", constants.STARTING_URL)
    while links_queue.size() > 0 and pages_crawled < constants.MAX_PAGES_TO_SCRAPE:
        scrape_from_queue()
    print(links_crawled)

# Start Crawling from here
start_crawling()
