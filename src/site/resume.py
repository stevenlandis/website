from src.parts.Elem import Elem, Favicon, StyleSheet
from src.parts.WebPage import WebPage

def ClassDiv(content, clss):
    return Elem('div', {'class': clss}, content)

def MainTitle(txt):
    return Elem('div', {'class': 'mainTitle'}, txt)

def Subtitle(txt):
    return Elem('div', {'class': 'subtitle'}, txt)

def HR():
    return Elem('hr', {'class': 'hr'})

def Section(left, right):
    leftSpan = Elem('div', {'class': 'leftSection'}, left)
    rightSpan = Elem('div', {'class': 'rightSection'}, right)

    return Elem('div', {'class': 'section'}, [leftSpan, rightSpan])

def SectionTitle(txt):
    return Elem('div', {'class': 'sectionTitle'}, txt)

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

def build():
    head = [
        Elem('title', {}, 'Resume'),
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        Favicon(16, 16),
        Favicon(32, 32),
        Favicon(96, 96),
        StyleSheet('resume_resources/resumeStyles.css'),
        '<style type="text/css" media="print">@page {size: auto;margin: 0;}</style>'
    ]

    content = [
        MainTitle('STEVEN LANDIS'),
        Subtitle('[FIRST][LAST] at comcast dot net'),
        Subtitle('Santa Barbara, CA'),
        HR(),
        Section(
            ClassDiv('EDUCATION', 'sectionTitle'),
            [
                SectionTitle('UNIVERSITY OF CALIFORNIA SANTA BARBARA'),
                SectionText('COMPUTER ENGINEERING | GRADUATION: JUNE 2020'),
                SectionText('GPA: 3.96')
            ]
        ),
        Section(
            ClassDiv('RELEVANT COURSEWORK', 'sectionTitle'),
            DualCol(
                [
                    SectionText('Data Structures and Algorithms (CS 130AB)'),
                    SectionText('Compilers (CS 160, CS 162)'),
                    SectionText('Arduino Programming (ECE 5)'),
                    SectionText('Analog Circuits (ECE 10ABC)')
                ],
                [
                    SectionText('Machine Learning (ECE 156AB)'),
                    SectionText('Digital Circuits (CS 40, ECE 15A, 152A)'),
                    SectionText('Verilog (ECE 152A, 156A)'),
                    SectionText('Embedded Systems (ECE 153AB)')
                ],
                ratio = 0.55)
        ),
        HR(),
        Section(
            ClassDiv('EXPERIENCES', 'sectionTitle'),
            [
                SectionTitle('SOFTWARE ENGINEER'),
                SectionText('RIDGELINE APPS. | SUMMER 2019'),
                SectionText('TYPESCRIPT AND REACT'),
                Bullets([
                    'Wrote a charting library from the ground up',
                    'Starting with no prior experience, became go-to person for questions about testing, React and Typescript in about 5 weeks',
                    'Used developer feedback to streamline chart-creation functions and make library easy to modify',
                    'Worked with other developers to integrate charts into main application'
                ]),
                HR(),
                SectionTitle('SOFTWARE ENGINEER'),
                SectionText('UCSB CHEMICAL ENGINEERING DEPT. | OCT 2017 – PRESENT'),
                SectionText('MATLAB'),
                TitledBullets(
                    'Ongoing Responsibilities:',
                    [
                        'Leading redesign of industrial crystal shape prediction software',
                        'Creating visualizations of complex crystallographic processes',
                        'Reviewing and improving coworker\'s algorithms to reduce runtime'
                    ]
                ),
                TitledBullets(
                    'Completed Responsibilities:',
                    [
                        'Quickly learned MATLAB and cutting-edge crystallography research despite no prior experience',
                        'Designed UI layout tools and UI',
                        'Taught coworkers revision control (GIT) and manged repository',
                        [
                            'GitHub Contributions: [',
                            Color('117,971++', 'green'),
                            ', ',
                            Color('22,572++', 'red'),
                            ']'
                        ]
                    ]
                ),
                HR(),
                SectionTitle('2-PIVOT DRAWING ARM PROJECT'),
                SectionText('IN CLASS ECE 5 | MARCH – APRIL 2017'),
                SectionText('PYTHON AND C'),
                Bullets([
                    'Worked in team of 3 to design, manufacture and program a mechanical arm that drew pictures with a pen',
                    'Designed and 3D printed pen holder using SolidWorks',
                    'Operated metal fabrication tools (lathe, drill press, tapping machine, band saw) to build arm from scratch',
                    'Programmed Python sketching program for computer',
                    'Wrote C program for Arduino to control 2 stepper motors and 1 servo motor to draw picture',
                    'Debugged serial connection between computer and Arduino'
                ]),
                HR(),
                SectionTitle('IEEE EXTREME CODING COMPETITION'),
                SectionText('OCTOBER 2017 – 24 HRS'),
                SectionText('C++ AND JAVASCRIPT'),
                Bullets([
                    'Used data structures (arrays, stacks, trees) to model and solve problems',
                    'Reduced computational complexity to reduce runtime within time limit',
                    'Ranked in top 7% of competitors (international college and graduate students)'

                ])
            ]
        ),
        HR(),
        Section(
            'PROGRAMMING LANGUAGES AND ENVIRONMENTS',
            DualCol(
                [
                    SectionText('Typescript React'),
                    SectionText('MATLAB'),
                    SectionText('C++'),
                    SectionText('JavaScript')
                ],
                [
                    SectionText('C'),
                    SectionText('BASH / Linux Terminal'),
                    SectionText('Python'),
                    SectionText('Verilog')
                ]
            )
        )
    ]


    body = Elem('div', {'class': 'mainContent'}, content)

    return WebPage(head, body)
