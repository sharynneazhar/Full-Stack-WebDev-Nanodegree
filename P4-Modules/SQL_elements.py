#
# Write a query that returns all the species in the zoo, and how many animals of
# each species there are, sorted with the most populous species at the top.
#
# The result should have two columns:  species and number.
#
# The animals table has columns (name, species, birthdate) for each individual.
#

QUERY = '''
select count(*) as num, species
    from animals
    group by species
    order by num desc
'''

# --------------------------------------------------------------------------------------------

#
# Insert a newborn baby opossum into the animals table and verify that it's been added.
# To do this, fill in the rest of SELECT_QUERY and INSERT_QUERY.
#
# SELECT_QUERY should find the names and birthdates of all opossums.
#
# INSERT_QUERY should add a new opossum to the table, whose birthdate is today.
# (Or you can choose any other date you like.)
#
# The animals table has columns (name, species, birthdate) for each individual.
#

SELECT_QUERY = "select name, birthdate from animals where species = 'opossums';"

INSERT_QUERY = "insert into animals values ('Wibble', 'opossum', '2016-06-16');"

# --------------------------------------------------------------------------------------------

#
#
# Find the names of the individual animals that eat fish.
#
# The animals table has columns (name, species, birthdate) for each individual.
# The diet table has columns (species, food) for each food that a species eats.
#

QUERY = '''
select name
    from animals, diet
    where animal.species = diet.species
        and diet.food = 'fish'
'''

# --------------------------------------------------------------------------------------------

#
# Find the one food that is eaten by only one animal.
#
# The animals table has columns (name, species, birthdate) for each individual.
# The diet table has columns (species, food) for each food that a species eats.
#

QUERY = '''
select food, count(animals.name) as num
    from diet, animals
    where diet.species = animals.species
    group by food
    having num = 1
'''

# --------------------------------------------------------------------------------------------

#
# List all the taxonomic orders, using their common names, sorted by the number of
# animals of that order that the zoo has.
#
# The animals table has (name, species, birthdate) for each individual.
# The taxonomy table has (name, species, genus, family, t_order) for each species.
# The ordernames table has (t_order, name) for each order.
#
# Be careful:  Each of these tables has a column "name", but they don't have the
# same meaning!  animals.name is an animal's individual name.  taxonomy.name is
# a species' common name (like 'brown bear').  And ordernames.name is the common
# name of an order (like 'Carnivores').

QUERY = '''
select ordernames.name, count(*) as num
    from animals, taxonomy, ordernames
    where animals.species = taxonomy.name
        and taxonomy.t_order = ordernames.t_order
    group by ordernames.name
    order by num desc
'''
