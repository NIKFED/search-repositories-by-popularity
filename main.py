import numpy as np
from github import Github
import matplotlib as mpl
import matplotlib.pyplot as plt
from terminaltables import GithubFlavoredMarkdownTable
import codecs

# Insert you username and password
g = Github("*", "*")

# Settings
number_of_reps = 10
names_of_props = ["Id", "Name", "Description", "Language", "Stars", "Forks"]
github_server_link = "https://github.com/"
md_file_name = 'result3dFrameworks.md'

# Main query
seach_query = g.search_repositories("3d", sort="stars", order="desc")
results = []
for index, rep in enumerate(seach_query):
    rep_prop = [index + 1]
    link = github_server_link + rep.full_name
    rep_prop.append("[{}]({})".format(rep.name, link))
    rep_prop.append(rep.description)
    rep_prop.append(rep.language)
    rep_prop.append(rep.stargazers_count)
    rep_prop.append(rep.forks)

    results.append(rep_prop)

    if (index > number_of_reps - 2):
        break

# Creating the table
table_data = [["" for x in range(len(names_of_props))] for y in range(number_of_reps + 1)]

for i in range(len(names_of_props)):
    table_data[0][i] = names_of_props[i]

for i in range(number_of_reps):
    for j in range(len(names_of_props)):
        table_data[i + 1][j] = results[i][j]

# Generating the ascii table
table = GithubFlavoredMarkdownTable(table_data)
table_str = table.table

# Wrting the md file
with codecs.open(md_file_name, "w", "utf-8") as f:
    f.write(table_str)

labels = [i[1] for i in table_data if i[0] != 'Id']
for i in range(len(labels)):
    labels[i] = labels[i].partition('(')[0]
    labels[i] = labels[i][1:len(labels[i]) - 1]

valueStar = [i[4] for i in table_data if i[0] != 'Id']
valueFork = [i[5] for i in table_data if i[0] != 'Id']

dpi = 80
fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
mpl.rcParams.update({'font.size': 9})

plt.title('Top 10 frameworks with the biggest stars and forks')

plt.grid(True, zorder = 1)

xs = range(len(labels))

plt.barh([x + 0.3 for x in xs], valueStar,
         height = 0.2, color = 'red', alpha = 0.7, label = 'Stars',
         zorder = 2)
plt.barh([x + 0.05 for x in xs], valueFork,
         height = 0.2, color = 'blue', alpha = 0.7, label = 'Forks',
         zorder = 2)
plt.yticks(xs, labels)

plt.legend(loc='upper right')
fig.savefig('result.png')
