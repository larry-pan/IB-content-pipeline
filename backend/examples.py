import generator


math_generator = generator.CSGenerator()
cs_generator = generator.CSGenerator()

# Examples
print(math_generator.generate(topic="Calculus"))
print(cs_generator.generate(topic="Networks"))
