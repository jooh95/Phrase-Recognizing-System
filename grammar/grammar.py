from pattern3.en import conjugate


verb = "go"
result = conjugate(verb,
                   tense="past",
                   person=3,
                   number="singular",
                   mood="indicative",
                   aspect="imperfective",
                   negated=False)
print(result)
