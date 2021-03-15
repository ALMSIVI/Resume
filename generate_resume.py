import argparse
import json
import os
from typing import Dict

parser = argparse.ArgumentParser(
    description='Create a LaTex resume file from a template.')
parser.add_argument('-l', '--language', default='en',
                    help='Language of the resume to generate.')
parser.add_argument('-o', '--output', default='resume.tex',
                    help='Output tex file.')

args = parser.parse_args()


# Read language-specific files
with open('data/resume-{}.json'.format(args.language), 'rt') as f:
    data = json.load(f)

with open('i18n/i18n-{}.json'.format(args.language), 'rt') as f:
    i18n = json.load(f)

# Read templates
templates: Dict[str, str] = {}
for filename in os.listdir('templates'):
    key = filename[:-4]
    contents = []
    with open(os.path.join('templates', filename), 'rt') as f:
        for line in f:
            contents.append(line)

    templates[key] = ''.join(contents)

with open(args.output, 'wt') as out:
    out.write(templates['declarations'])
    out.write(templates['begin'])

    # Header
    section = data['info']
    text = templates['header']
    for key in section:
        text = text.replace('%' + key, section[key])
    out.write(text)

    # Comment
    section = data['comments']
    text = templates['comments'].replace('%comment', section['position'])
    if section['include']:
        out.write(text)

    # Education
    text = templates['section'].replace('%sectext', i18n['education'])
    out.write(text)

    section = data['education']
    text = templates['education'] \
        .replace('%name', section['name']) \
        .replace('%bsdate', section['bsdate']) \
        .replace('%bsgpa', section['bsgpa']) \
        .replace('%bs', section['bs']) \
        .replace('%msdate', section['msdate']) \
        .replace('%msgpa', section['msgpa']) \
        .replace('%ms', section['ms'])
        
    out.write(text)

    # Skills
    text = templates['section'].replace('%sectext', i18n['skill'])
    out.write(text)

    section = data['skills']
    text = templates['skills'] \
        .replace('%langtext', i18n['language']) \
        .replace('%frametext', i18n['framework']) \
        .replace('%softtext', i18n['software'])

    def generate_skill(skill):
        '''
        Needs to replace # to \\# in LaTeX. Also, make LaTex beautiful.
        '''
        return skill['name'].replace('#', '\\#').replace('LaTeX', '\\LaTeX')

    languages = ', '.join(map(generate_skill, section['language']))
    frameworks = ', '.join(map(generate_skill, section['framework']))
    software = ', '.join(map(generate_skill, section['software']))
    text = text \
        .replace('%languages', languages) \
        .replace('%frameworks', frameworks) \
        .replace('%software', software)
    out.write(text)

    def generate_bullet(bullet):
        return templates['item'].replace('%item', bullet)

    # Work
    text = templates['section'].replace('%sectext', i18n['work'])
    out.write(text)

    def generate_work(work):
        return templates['work'] \
            .replace('%position', work['position']) \
            .replace('%company', work['company']) \
            .replace('%location', work['location']) \
            .replace('%date', work['date']) \
            .replace('%bullets', '\n'.join(map(generate_bullet, work['bullets'])))

    section = data['work']
    for work in section:
        out.write(generate_work(work))

    # Projects
    text = templates['section'].replace('%sectext', i18n['project'])
    out.write(text)

    def generate_project(project):
        return '' if project['hide'] else templates['project'] \
            .replace('%name', project['name']) \
            .replace('%position', project['position']) \
            .replace('%date', project['date']) \
            .replace('%bullets', '\n'.join(map(generate_bullet, project['bullets'])))

    section = data['projects']
    for project in section:
        out.write(generate_project(project))

    out.write(templates['end'])
