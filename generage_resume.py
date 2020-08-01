import json

with open('resume.json', 'r') as f:
    resume = json.load(f)

with open('template.json', 'r') as f:
    template = json.load(f)

info = template['info'].format(resume['info']['name'], resume['info']['email'],
                               resume['info']['phone'], resume['info']['github'], resume['info']['linkedin'])

comments = template['comments'].format(
    resume['comments']['position']) if resume['comments']['include'] else ''

education = template['education'].format(resume['education']['name'], resume['education']['time'],
                                         resume['education']['degree'], resume['education']['gpa'], ', '.join(resume['education']['courses']))

# Need to escape 'C#' to 'C\#' and 'LaTeX' to '\LaTeX'
for i in range(len(resume['skills']['language'])):
    if resume['skills']['language'][i] == 'C#':
        resume['skills']['language'][i] = 'C\\#'
    elif resume['skills']['language'][i] == 'LaTeX':
        resume['skills']['language'][i] = '\\LaTeX'

skills = template['skills'].format(', '.join(resume['skills']['language']), ', '.join(
    resume['skills']['framework']), ', '.join(resume['skills']['software']))


def generate_work(project):
    return template['work']['project'].format(project['position'], project['company'], project['location'], project['date'], ''.join(map(lambda bullet: template['work']['bullet'].format(bullet), project['bullets'])))


work = template['work']['template'].format(
    ''.join(map(generate_work, resume['work'])))


def generate_project(project):
    return '' if project['hide'] else template['projects']['project'].format(project['name'], project['position'], project['date'], ''.join(map(lambda bullet: template['projects']['bullet'].format(bullet), project['bullets'])))


projects = template['projects']['template'].format(
    ''.join(map(generate_project, resume['projects'])))

string = template['template'].format(
    info, comments, education, skills, work, projects)

with open('resume.tex', 'w') as f:
    f.write(string)
