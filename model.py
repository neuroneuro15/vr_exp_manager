from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Time, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from collections import namedtuple


Base = declarative_base()

class Experiment(Base):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    def __repr__(self):
        return "<Experiment(name='{}')>".format(self.name)


class Experimenter(Base):
    __tablename__ = 'experimenters'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return "<Experimenter(name='{}')>".format(self.name)


class Rat(Base):
    __tablename__ = 'rats'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    birthdate = Column(Date)

    def __repr__(self):
        return "<Rat(name='{}')>".format(self.name)


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)
    experimenter_id = Column(Integer, ForeignKey('experimenters.id'), nullable=False)
    rat_id = Column(Integer, ForeignKey('rats.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    video_filename = Column(String)
    motive_take_filename = Column(String)

    experiment = relationship("Experiment", back_populates='sessions')
    experimenter = relationship("Experimenter", back_populates='sessions')
    rat = relationship("Rat", back_populates='sessions')

    def __repr__(self):
        return "<Session(date={}, rat={}, experiment={})>".format(self.date, self.rat.name, self.experiment.name)

for tbl in (Experiment, Experimenter, Rat):
    tbl.sessions = relationship('Session', order_by=Session.date, back_populates=tbl.__name__.lower())


class Condition(Base):
    __tablename__ = 'conditions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)

    experiment = relationship("Experiment", back_populates='conditions')

    def __repr__(self):
        return "<Condition(experiment='', name='{}')>".format(self.experiment.name, self.name)

for tbl in (Experiment,):
    tbl.conditions = relationship('Condition', order_by=Condition.name, back_populates=tbl.__name__.lower())


class Level(Base):
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)




class TrackingObject(Base):
    __tablename__ = 'trackingobjects'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    system = Column(String)

    def __repr__(self):
        return "<TrackingObject(name='{}', system='{}')>".format(self.name, self.system)


Position = namedtuple('Position', 'x y z')
RotationEuler = namedtuple('RotationEuler', 'x y z')
RotationQuaternion = namedtuple('RotationQuaternion', 'x y z w')
Orientation = namedtuple('Orientation', 'x y z')

class TrackingDataPoint(Base):
    __tablename__ = 'trackingdata'

    id = Column(Integer, primary_key=True)
    condition_id = Column(Integer, ForeignKey('conditions.id'))
    session_id = Column(Integer, ForeignKey('sessions.id'))
    trackingobject_id = Column(Integer, ForeignKey('trackingobjects.id'))
    time = Column(Time, nullable=False)
    motive_timestamp = Column(Integer)
    is_visible = Column(Boolean)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    rot_x = Column(Float)
    rot_y = Column(Float)
    rot_z = Column(Float)
    rot_qx = Column(Float)
    rot_qy = Column(Float)
    rot_qz = Column(Float)
    rot_qw = Column(Float)
    ori_x = Column(Float)
    ori_y = Column(Float)
    ori_z = Column(Float)

    condition = relationship('Condition', back_populates='trackingdata')
    session = relationship('Session', back_populates='trackingdata')
    trackingobject = relationship('TrackingObject', back_populates='trackingdata')


    def __repr__(self):
        return "<TrackingDataPoint(trackingobject='{}', session={}, time={}, position={}, rotation={})>".format(
            self.trackingobject.name, self.time, self.position[:], self.rotation[:])


    @property
    def position(self):
        return Position(x=self.x, y=self.y, z=self.z)

    @position.setter
    def position(self, value):
        self.x, self.y, self.z = value

    @property
    def rotation(self):
        return RotationEuler(x=self.rot_x, y=self.rot_y, z=self.rot_z)

    @rotation.setter
    def rotation(self, value):
        self.rot_x, self.rot_y, self.rot_z = value

    @property
    def rotation_quaternion(self):
        return RotationQuaternion(x=self.rot_qx, y=self.rot_qy, z=self.rot_qz, w=self.rot_qw)

    @rotation_quaternion.setter
    def rotation_quaternion(self, value):
        self.rot_qx, self.rot_qy, self.rot_qz, self.rot_qw = value

    @property
    def orientation(self):
        return Orientation(x=self.ori_x, y=self.ori_y, z=self.ori_z)

    @orientation.setter
    def orientation(self, value):
        self.ori_x, self.ori_y, self.ori_z = value

for tbl in (Session, TrackingObject, Condition):
    tbl.trackingdata = relationship('TrackingDataPoint', order_by=TrackingDataPoint.time, back_populates=tbl.__name__.lower())

