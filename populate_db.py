from itertools import cycle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Rat, Experiment, Experimenter, Condition
from datetime import date, time

engine = create_engine('sqlite:///testdb.db')


sqlsession = sessionmaker(bind=engine)()

# Add Rats
for cage, letter in zip(range(2, 12), cycle('AB')):
    rat = Rat(name='VR-{}{}'.format(cage // 2, letter), birthdate=date(2017, 2, 15))
    sqlsession.add(rat)
sqlsession.commit()

# Add Experimenters
for name in ('Nicholas A. Del Grosso', 'Eduardo Blanco Hernandez'):
    person = Experimenter(name=name)
    sqlsession.add(person)
sqlsession.commit()

# Add Experiments
cliffexp_desc = """Look for cliff avoidance behavior
jump to side of arena away from cliff) in ratCAVE VR sessions,
when the cliff is virtual, real (nonreflective plastic over actual hole in arena),
or a static (non-VR, non-moving) projection."""
cliffexp = Experiment(name='Virtual Cliff Exp', description=cliffexp_desc)


objexp_desc = """Look for exploration of an"""
objexp = Experiment(name='Virtual Object Preference Exp', description=objexp_desc)

wallexp_desc = """Look for exploration of an"""
wallexp = Experiment(name='Virtual Wall Thigmotaxis Exp', description=wallexp_desc)

for exp in (cliffexp, objexp, wallexp):
    sqlsession.add(exp)
sqlsession.commit()


# Add Experimental Conditions
for name, desc in [('Real Cliff', 'An actual cliff'), ('VR Cliff', 'VR-Projected Cliff'), ('Static', 'A Cliff projected, but not updated.')]:
    condition = Condition(name=name, description=desc, experiment=cliffexp)
    sqlsession.add(condition)

for name, desc in [('InitialExploration', 'The first minute in the arena.  No wall pattern, no objects presented.'),
                   ('WallPatternA', '2nd phase: Arena wall pattern projected.  No objects presented, no object exploration bias expected.'),
                   ('VirtualObject_Left', 'Virtual Object presented on Left position, including arena wall pattern.'),
                   ('VirtualObject_Right', 'Virtual Object presented on Right position, including arena wall pattern.'),
                   ('RealObject_Left', 'Real Object presented on Left position, including arena wall pattern.'),
                   ('RealObject_Right', 'Real Object presented on Right Position, including arena wall pattern.'),]:
    condition = Condition(name=name, description=desc, experiment=cliffexp)
    sqlsession.add(condition)


sqlsession.commit()

