import inflect

def pluralize(word):
  engine = inflect.engine()
  plural = engine.plural(word)
  return(plural)
