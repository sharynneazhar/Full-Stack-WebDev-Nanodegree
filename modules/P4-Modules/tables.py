#
# Roommate Finder v0.9
#
# This query is intended to find pairs of roommates.  It almost works!
# There's something not quite right about it, though.  Find and fix the bug.
#

QUERY = '''
select a.id, b.id,
    a.building, a.room
from residences as a,
    residences as b
where a.building = b.building
    and a.room = b.room
    and a.id < b.id
order by a.building, a.room;
'''

#
# To see the complete residences table, uncomment this query and press "Test Run":
#
# QUERY = "select id, building, room from residences;"
#

# --------------------------------------------------------------------------------------------

# In this quiz, there's a table describing bugs in various files of code.
# Here's what the table looks like:
#
# create table programs (
#    name text,
#    filename text
# );
# create table bugs (
#    filename text,
#    description text,
#    id serial primary key
# );
#
# The query below is intended to count the number of bugs in each program. But
# it doesn't return a row for any program that has zero bugs.  Try running it as
# it is; then change it so that it includes rows for the programs with no bugs.

QUERY = '''
select programs.name, count(bugs.filename) as num
   from programs left join bugs
        on programs.filename = bugs.filename
   group by programs.name
   order by num;
'''

# --------------------------------------------------------------------------------------------

# Find the players whose weight is less than the average.
#
# The function below performs two database queries in order to find the right players.
# Refactor this code so that it performs only one query.
#

def lightweights(cursor):
    """Returns a list of the players in the db whose weight is less than the average."""
    cursor.execute("select avg(weight) as av from players;")
    av = cursor.fetchall()[0][0]  # first column of first (and only) row
    cursor.execute("select name, weight from players where weight < " + str(av))
    return cursor.fetchall()

QUERY = '''
select name, weight
    from players,
        (select avg(weight) as av
            from players) as subq
    where weight < av;
'''
