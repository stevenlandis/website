from src.parts.defs import Page, Script

def build(builder):
    head = [
        Script('pr.js', builder),
        Script('SharedValue.js', builder),
        Script('wait.js', builder),
        Script('Deferred.js', builder),
        Script('BaseElem.js', builder),
        Script('animate.js', builder),
        Script('mount.js', builder),
        Script('test.js', builder),
        Script('main.js', builder)
    ]

    return Page('Script Test', head, '')