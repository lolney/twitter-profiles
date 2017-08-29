from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.engine.url import URL
import re, os

"""
Base = declarative_base()
class Categorylinks(Base):

    __tablename__ = 'categorylinks'
    cl_from = Column(Integer(), primary_key=True)
    cl_to = Column(String())
    cl_sortkey = Column(String())
    cl_timestamp = Column(String())
"""
class Categorylinks(object):
    pass

class Page(object):
    pass

def create_sessionmaker():
    url = URL('mysql', username='root', password=os.environ.get("ENWIKIPASSWORD", None), host='localhost', database='enwiki')
    classnames = [Categorylinks, Page]
    names = ['categorylinks', 'page']

    engine = create_engine(url, echo=True)
    Base.metadata.create_all(engine)
 
    metadata = MetaData(engine)
    for classname, name in zip(classnames, names):
        table = Table(name, metadata, autoload=True)
        mapper(classname, table)
 
    Session = sessionmaker(bind=engine)
    return Session

Base = declarative_base()
class FilteredCategory(Base):

    __tablename__ = 'filteredcategories'

    page_id = Column(Integer)
    subcat_id = Column(Integer, primary_key=True)
    subcat = Column(String(255))

class User(Base):

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255))
    categories = Column(JSON)

class Interests(Base):
    __tablename__ = 'interests'

    user_id = Column(Integer)
    interest = Column(String(255), primary_key=True)
    weight = Column(Integer)

Session = create_sessionmaker()

class Category():

    def __init__(self, name, parent=None, decay_factor=1):
        self.name = name
        self.parent = parent
        self.count = 1
        self.children = None
        self.decay_factor = decay_factor

    def inc(self):
        self.count = count + (1 * self.decay_factor)

    def add_child(self, child):
        if self.children is None:
            self.children = []
        self.children.append(child)

class DBSession():

    def __init__(self):
        self.session = Session()

    # From a list of candidate strings, find the root candidates and significance counts
    def categories_from_candidates(self, candidates):
        #trailingws = re.compile('\s+$')
        ws = re.compile('\s+')
        candidates_formated = [re.sub(ws, "_") for c in candidates]
        cmap = {}
        for candidate in candidates_formated:
            if cmap[candidate] is None:
                cmap[candidate] = self.traverse_up(candidate)
            else:
                self.traverse_up_objects(cmap[candidate])
        return self.find_children(cmap)

    def find_children(self, candidate_map):
        root_cats = []
        for name, cat in candidate_map.iteritems():
            for child_name, child_cat in cmap.iteritems():
                if child_cat.parent is not None:
                    if child_cat.parent.name == name:
                        cat.add_child(child_cat)
            if cat.parent is None:
                root_cats.append(cat)

                
    def traverse_up(self, text):
        # Find category links with that page id; these are parent categories
        superclass = self.session.query(FilteredCategory).filter_by(subcat = text).one_or_none()
        if superclass is None: # no supercategories
            return Category(name=text)
        else:
            return Category(name=text,parent=traverse_up(session, cat.cl_to))

    def traverse_up_objects(self, cat):
        if cat is not None:
            cat.inc()
            traverse_up_objects(cat.super)

    def traverse_down(self, visited, supercat_id, supercat):
        # 14 is the category namespace; 0 is the page namespace
        subcat_ids = [s.cl_from for s in self.session.query(Categorylinks).filter_by(cl_to = supercat)]
        for subcat_id in subcat_ids:
            if subcat_id not in visited:
                visited.add(subcat_id)
                # Look up page title
                subcat = self.session.query(Page).filter_by(page_id = subcat_id).one().page_title
                self.session.add(FilteredCategory(page_id=supercat_id, subcat=subcat, subcat_id=subcat_id))
                self.traverse_down(visited, subcat_id, subcat)
                
    # Seed top level categories
    def createCats(self):
        seeds = ["Research","Culture","Arts","Places","Geography","Health","Self_care","Healthcare_occupations","History","Events","Formal_sciences","Natural_sciences","People","Personal_life","Self","Philosophy","Thought","Religion","Technology","Society"]
        visited = set()
        for seed in seeds:
            page_id = self.session.query(Page).filter_by(page_title = seed).filter_by(page_namespace = 14).one().page_id
            visited.add(page_id)
            self.traverse_down(visited, page_id, seed)

        self.session.commit()
        print self.session.query(FilteredCategory).limit(10)

    def create_user(self, username, user_id, categories):
        user = User(username=username, user_id=user_id, categories=categories)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self, user_id):
        return self.session.query(User).filter_by(user_id = user_id).one_or_none()

    def getCategories(self):
        return self.session.query(Categorylinks).join(Page, Page.page_id==Categorylinks.cl_from).limit(10)

    def getPage(self, title):
        return self.session.query(Page).filter_by(page_title = title).one()

def categories(candidates):
    session = DBSession()
    return session.categories_from_candidates()

if __name__ == "__main__":
    session = DBSession()
    print session.createCats()