"""Course: CIS 640 ZA
    Assignment: Develop A Python Project
    Author: Zachary Cleary"""


class Network(object):
    """A network of people and relationships"""

    def __init__(self):
        """Construct an instance of Network"""
        # constructor
        self.people = {}
        self.relations = {}
        self.names = {}
        self.counter = 0

    def create_person(self):
        """Create a person in the network and return the person"""
        p = Person(self.counter)
        self.people[p.id] = p
        self.counter += 1
        return p

    def add_person_property(self, person, prop, value):
        """Add the given property to the given person"""
        # raise error if the given person is None or not in the network
        if (person is None) or (person.id not in self.people):
            raise RuntimeError

        # raise error if given the name property and it is already in use in the network
        if prop == 'name':
            for x in self.people.values():
                if x.id == person.id:
                    # id's match because it is the same person - ignore
                    continue
                if not x.property.get('name') is None and x.property['name'] == value:
                    # found two different people with the same name - raise error
                    raise RuntimeError
                # map the name to the person's id - to assist in looking up either by id or name later
                self.names[value] = person.id
        # set the property with the given value
        person.property[prop] = value

    def add_relation(self, person1, person2):
        """Add a new relation between the given persons"""
        # raise error if either person is None
        if person1 is None or person2 is None:
            raise RuntimeError

        # raise error if the given person is not in the network
        if person1.id not in self.people or person2.id not in self.people:
            raise RuntimeError

        # raise error if a relation already exists between the given people
        relationPairs = {r.person1: r.person2 for r in self.relations.values()}
        for p1 in relationPairs:
            # remember that order doesn't matter - check both combinations
            if (p1 is person1 and relationPairs[p1] is person2) or (p1 is person2 and relationPairs[p1] is person1):
                raise RuntimeError

        # both people check out and there isn't yet a relation - create a relation between them
        r = Relation(person1, person2)
        self.relations[r.key] = r
        return r

    def add_relation_property(self, person1, person2, prop, value):
        """Add a property to the relation that exists between the given persons"""
        # raise error if either person is null
        if person1 is None or person2 is None:
            raise RuntimeError

        # add the relation property if a relationship exists between the given persons
        relation = self.get_relation(person1, person2)
        if relation is not None:
            if prop == 'friend' and not self.isFriends(person1, person2):
                # if given the friendship property and they aren't yet friends, make them friends
                person1.friends.append(person2)
                person2.friends.append(person1)
            relation.property[prop] = value

    def isFriends(self, person1, person2):
        """Return True if the two people are friends else return False"""
        for relation in self.relations.values():
            # relationships are not order-dependent
            if (relation.person1 is person1 and relation.person2 is person2) or \
                    (relation.person1 is person2 and relation.person2 is person1):
                # if a matching couple was found and the friend property exists between them, return True
                if relation.property.get('friend') is not None:
                    return True
        return False

    def get_person(self, name):
        """Return the person with the given name if it exists, else raise RuntimeError"""
        targetId = self.names.get(name)
        if targetId is not None:
            return self.people[targetId]
        else:
            raise RuntimeError

    def friends_of_friends(self, name):
        """Return a list of the friends of friends of the person with the given name"""
        person = self.get_person(name)
        friendsOfPerson = person.friends
        friendsOfFriendsOfPerson = []
        for i in friendsOfPerson:
            for j in i.friends:
                friendsOfFriendsOfPerson.append(j)
        return list(set(friendsOfFriendsOfPerson))

    def get_relation(self, person1, person2):
        """Return the relation between the persons if one exists, else return None"""
        for relation in self.relations.values():
            if (relation.person1 is person1 and relation.person2 is person2) or \
                    (relation.person1 is person2 and relation.person2 is person1):
                return relation
        return None


class Person(object):
    """A person in the network"""
    def __init__(self, num):
        """Constructs an instance of Person"""
        self.property = {}
        self.id = num
        self.friends = []

    def add_property(self, prop, value):
        """Adds the given property to this Person"""
        if prop == "friends":
            self.friends.append(value)
        self.property[prop] = value


class Relation(object):
    """A relation between two people (or a person and himself) in the network"""
    # static counter used to ensure unique id's for Relation objects
    curId = 0

    def __init__(self, person1, person2):
        """Constructs an instance of Relation"""
        self.property = {}
        self.key = Relation.curId
        Relation.curId += 1
        self.person1 = person1
        self.person2 = person2

    def add_property(self, prop, value):
        """Adds the given property to this Relation"""
        # add the given property
        self.property[prop] = value
