from crawler import StackOverflow

page = open('stackoverflow.html').read();
print page
print StackOverflow._parse_results(page)
