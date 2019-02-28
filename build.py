from pybuilder.core import use_plugin, init

use_plugin("python.core")
# use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "ScrapingTask"
version="1.0"
default_task = "publish"

summary="Web Scraping and Crawling"


@init
def set_properties(project):
    pass
