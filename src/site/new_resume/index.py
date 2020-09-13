from src.parts.Elem import Elem, Favicon, StyleSheet
from src.parts.WebPage import WebPage
from json import loads
import bld
from math import ceil

def join(lst, sep):
  res = [sep] * (2*len(lst)-1)
  for i in range(len(lst)): res[2*i] = lst[i]
  return res

def andJoin(lst):
  res = [None] * (2*len(lst)-1)
  for i in range(len(lst)): res[2*i] = lst[i]
  for i in range(len(lst)-1):
    res[2*i+1] = ' and ' if i == len(lst)-2 else ', '
  return res

def ClassDiv(content, clss):
  return Elem('div', {'class': clss}, content)

def MainTitle(txt):
  return Elem('div', {'class': 'mainTitle'}, txt.upper())

def Subtitle(txt):
  return Elem('div', {'class': 'subtitle'}, txt)

def HR():
  return Elem('hr', {'class': 'hr'})

def VSpacer():
  return Elem('div', {'class': 'vSpacer'})

def Section(left, right):
  leftSpan = Elem('div', {'class': 'leftSection'}, left)
  rightSpan = Elem('div', {'class': 'rightSection'}, right)

  return Elem('div', {'class': 'section'}, [leftSpan, rightSpan])

def SectionTitle(txt):
  return Elem('div', {'class': 'sectionTitle'}, txt.upper())

def SectionSubTitle(txt):
  return ClassDiv(txt.upper(), 'sectionText')

def SectionText(txt):
  return ClassDiv(txt, 'sectionText')

def DualCol(left, right, ratio = 0.5):
  leftPercent = round(ratio*100)
  leftCol = Elem('div', {'style': f'width: {leftPercent}%;', 'class': 'column'}, left)
  rightCol = Elem('div', {'style': f'width: {100 - leftPercent}%;', 'class': 'column'}, right)
  return ClassDiv([leftCol, rightCol], 'dualColumn')

def Bullets(points):
  bullets = [Elem('li', {}, point) for point in points]
  return Elem('ul', {'class': 'bullets'}, bullets)

def TitledBullets(title, points):
  return ClassDiv([Elem('div', {}, title), Bullets(points)], 'titledBullets')

def Color(txt, color):
  return Elem('span', {'style': f'color: {color}'}, txt)

def Italics(txt):
  return Elem('em', txt)

def Course(course):
  return SectionText(f"{course['name']} ({course['code']})")

def Education(education):
  nLeft = ceil(len(education['coursework'])/2)
  leftCourses = education['coursework'][:nLeft]
  rightCourses = education['coursework'][nLeft:]
  return [
    Section(
      SectionTitle('Education'),
      [
        SectionTitle(education['name']),
        SectionText(education['major'].upper() + ' | GRADUATED: ' + education['graduation'].upper()),
        SectionText(f'GPA: {education["GPA"]}')
      ]),
    VSpacer(),
    Section(
      SectionTitle('Relevant Coursework'),
      DualCol(
        [Course(course) for course in leftCourses],
        [Course(course) for course in rightCourses],
        ratio = 0.5)),
  ]

def Experience(experience):
  res = []
  if 'name' in experience: res.append(SectionTitle(experience['name']))
  subtitle = []
  if 'location' in experience: subtitle.append(experience['location'])
  if 'date' in experience: subtitle.append(experience['date'])
  if len(subtitle) > 0: res.append(SectionSubTitle(' | '.join(subtitle)))
  if 'languages' in experience: res.append(SectionSubTitle(', '.join(experience['languages'])))
  if 'github contributions' in experience:
    res.append([
      'Github Contributions: [',
      Color(experience['github contributions']['additions'] + '++', 'green'),
      ', ',
      Color(experience['github contributions']['deletions'] + '--', 'red'),
      ']'])
  if 'accomplishments' in experience:
    res.append(Bullets(experience['accomplishments']))
  return res

def Experiences(experiences):
  return Section(
    SectionTitle('Experiences'),
    join([Experience(experience) for experience in experiences], HR()))

def Languages(languages):
  nLeft = ceil(len(languages)/2)
  leftLanguages = languages[:nLeft]
  rightLanguages = languages[nLeft:]
  return Section(
    SectionTitle('Programming Languages and Environments'),
    DualCol(
      [SectionText(language) for language in leftLanguages],
      [SectionText(language) for language in rightLanguages]))

def Paper(paper):
  return Elem('span', {'class': 'paper'}, join([
    andJoin(paper['authors']),
    f'"{paper["title"]}"',
    Italics(paper['journal']),
    paper['volume'],
    paper['page'],
    f'({paper["date"]})'
  ], ', ') + ['.'])

def Papers(papers):
  return Section(
    SectionTitle('Scientific Papers'),
    join([Paper(paper) for paper in papers], VSpacer()))

def Resume(resume):
  return Elem('div', {'class': 'mainContent'}, [
    MainTitle(resume['name']),
    Subtitle(resume['email']),
    Subtitle(resume['location']),
    HR(),
    Education(resume['education'],),
    HR(),
    Languages(resume['languages']),
    HR(),
    Experiences(resume['experiences']),
    HR(),
    Papers(resume['papers']),
  ])

def build():
  head = [
    Elem('title', 'Resume'),
    Favicon(16, 16),
    Favicon(32, 32),
    Favicon(96, 96),
    StyleSheet('resumeStyles.css'),
  ]

  data = loads(bld.File('resume.json').read())

  body = Resume(data)

  return WebPage(head, body)
