from src.parts.defs import Page, Script

def build(builder):
    head = [
        Script('pr.js', builder),
        Script('Depend.js', builder),
        Script('Wait.js', builder),
        Script('run.js', builder),
        Script('BaseElem.js', builder),
        Script('Elem.js', builder),
        Script('animate.js', builder),
        Script('test.js', builder),
        Script('main.js', builder)
    ]

    return Page('Script Test', head, '')