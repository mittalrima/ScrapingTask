import urllib.parse
import requests
import os
import bs4


def get_request(url):
    if is_absolute_url(url):
        try:
            r = requests.get(url)
            if r.status_code == 404 or r.status_code == 403:
                r = None
        except Exception:
            r = None
    else:
        r = None

    return r


def read_request(request):
    try:
        return request.text.encode('iso-8859-1')
    except Exception:
        print("read failed: " + request.url)
        return ""


def get_request_url(request):
    return request.url


def is_absolute_url(url):
    if url == "":
        return False
    return urllib.parse.urlparse(url).netloc != ""


def remove_fragment(url):
    (url, frag) = urllib.parse.urldefrag(url)
    return url


def convert_if_relative_url(current_url, new_url):
    if new_url == "" or not is_absolute_url(current_url):
        return None

    if is_absolute_url(new_url):
        return new_url

    parsed_url = urllib.parse.urlparse(new_url)
    path_parts = parsed_url.path.split("/")

    if len(path_parts) == 0:
        return None

    ext = path_parts[0][-4:]
    if ext in [".edu", ".org", ".com", ".net"]:
        return "http://" + new_url
    elif new_url[:3] == "www":
        return "http://" + new_path
    else:
        return urllib.parse.urljoin(current_url, new_url)


def is_url_ok_to_follow(url, limiting_domain):

    if "mailto:" in url:
        return False

    if "@" in url:
        return False

    if url[:LEN_ARCHIVES] == ARCHIVES:
        return False

    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme != "http" and parsed_url.scheme != "https":
        return False

    if parsed_url.netloc == "":
        return False

    if parsed_url.fragment != "":
        return False

    if parsed_url.query != "":
        return False

    loc = parsed_url.netloc
    ld = len(limiting_domain)
    trunc_loc = loc[-(ld+1):]
    if not (limiting_domain == loc or (trunc_loc == "." + limiting_domain)):
        return False

    # does it have the right extension
    (filename, ext) = os.path.splitext(parsed_url.path)
    return (ext == "" or ext == ".html")


def is_subsequence(tag):
    return isinstance(tag, bs4.element.Tag) and 'class' in tag.attrs \
        and tag['class'] == ['courseblock', 'subsequence']


def is_whitespace(tag):
    return isinstance(tag, bs4.element.NavigableString) and (tag.strip() == "")


def find_sequence(tag):
    rv = []
    sib_tag = tag.next_sibling
    while is_subsequence(sib_tag) or is_whitespace(tag):
        if not is_whitespace(tag):
            rv.append(sib_tag)
        sib_tag = sib_tag.next_sibling
    return rv
