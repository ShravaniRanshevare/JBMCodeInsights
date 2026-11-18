from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Date,Numeric

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True)
    user_email = Column(String)
    hashed_password = Column(String)
    
    
    
class Project(Base):
    __tablename__ = 'project' 
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    name= Column(String)
    created_at = Column(Date)
    


class FileRef(Base):
    __tablename__ = 'fileref'
    id = Column(Integer,primary_key=True,index=True)
    proj_id = Column(Integer,ForeignKey("project.id",ondelete="CASCADE"))
    filename = Column(String)
    file_path = Column(String,unique=True)
    uploaded_at = Column(Date)
    
class Analysis(Base):
    __tablename__ = 'analysis'
    
    id = Column(Integer,primary_key=True,index=True)
    proj_id = Column(Integer,ForeignKey("project.id",ondelete="CASCADE"))
    file_id = Column(Integer,ForeignKey("fileref.id",ondelete= "CASCADE")) #changed
    complexity_score = Column(Numeric(10,2))
    maintainability_score = Column(Numeric(10,2))
    retries = Column(Integer)
    
class Metrics(Base):
    __tablename__ = 'metrics'
    id = Column(Integer,primary_key=True,index=True)
    analysis_id = Column(Integer,ForeignKey("analysis.id",ondelete="CASCADE"))
    cognitive_score = Column(Numeric(10,2))
    cyclomatic_score = Column(Numeric(10,2))
    halstead_volume = Column(Numeric(10,2))
    loc = Column(Numeric(10,2))
    maintainability_index = Column(Numeric(10,2))
    cbo = Column(Numeric(10,2))
    lcom = Column(Numeric(10,2))
    depth = Column(Numeric(10,2))
    
class Refactorisations(Base):
    __tablename__ = 'refactorisations'
    id = Column(Integer,primary_key=True,index=True)
    analysis_id = Column(Integer,ForeignKey("analysis.id",ondelete="CASCADE")) 
    recommendations = Column(String)
    refactored_code = Column(String)
    complexity_after = Column(Numeric(10,2))
    maintainability_after= Column(Numeric(10,2))
    generated_at = Column(Date)
    


    