
import requests
import re
import csv

csv_content = []

# Github considers all pull requests to be issues but not all issues to be pull requests.
# Here we will construct a list of all issues which are not pull requsts. This is used for comparison in the future.
# becasue based on the problem formulation these issues which are also pull requests should not be added.
# we could have just checked this when fetching an issue instead of building this set, but that would require
# too many github api requests which is limited. And also this does not waste too much memory.

all_issues=set()

# store all the issues. This will be used later to check if a mentioned reference is a pullre quest or an issue.
for page in range(59):
    if(page%10==0):
        print('issue page',page)

    r = requests.get('https://api.github.com/repos/python/mypy/issues?state=all&is:issue&per_page=100&page='+str(page),auth=('sepehrjng92','0a0c97e1a873059ec02fd696b406898fd8c321a4'))

    for issue in range(len(r.json())):
        if(not "pull_request" in r.json()[issue].keys()):# check if the issue is a pull request
            all_issues.add(r.json()[issue]['number'])

for page in range(40): # 40 pages of pull requests
    if(page%10==0):
        print('pull request page',page)

    r = requests.get('https://api.github.com/repos/python/mypy/pulls?state=all&per_page=100&page='+str(page),auth=('sepehrjng92','0a0c97e1a873059ec02fd696b406898fd8c321a4'))
    for pull in range(len(r.json())): # 100 pulls per page

        # if (page%10==0 and pull % 10 == 0):
        #     print('pull number', pull)
        # print(r.json()[pull]['number'])
        content = r.json()[pull]['body']
        if(content ==None):
            continue
        issues = set(re.findall("#[0-9]+", content))

        string_list =['pr_#'+str(r.json()[pull]['number'])]
        for issue in issues:
            if(int(issue[1:]) in all_issues): # sometimes these numbers refer to other pull requests but we just want the issues.
                                              # so we need to check if this is the issue. Since we use a set, the lookup time is constant.
                string_list.append('issue_' + issue)

        if(len(string_list)>1): # has at least one issue which is not another pull request
            csv_content.append(string_list)

f = open('issues.csv', 'w')
w = csv.writer(f, delimiter=',')
w.writerows(csv_content)
f.close()
