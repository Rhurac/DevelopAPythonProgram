import impl


class TestNetwork(object):
    def __init__(self):
        self.t = TestAddPersonProperty()
        self.t1 = TestAddRelation()
        self.t2 = TestAddRelationProperty()
        self.t3 = TestGetPerson()
        self.t4 = TestFriendsOfFriends()

    def execute(self):
        self.t.test_property_is_overwritten()
        self.t.test_property_is_overwritten()
        self.t.test_raises_if_person_not_in_network()
        self.t.test_raises_if_name_already_in_network()
        self.t.test_raises_if_given_person_is_null()

        self.t1.test_raises_if_relation_already_exists()
        self.t1.test_raises_if_person1_not_exists()
        self.t1.test_raises_if_person2_not_exists()
        self.t1.test_relation_is_added_if_person1_equals_person2()
        self.t1.test_relation_is_added_if_person1_not_equals_person2()

        self.t2.test_property_added_if_person1_equals_person2()
        self.t2.test_property_added_if_person1_not_equals_person2()
        self.t2.test_property_value_gets_overwritten()
        self.t2.test_raises_if_person1_not_in_network()
        self.t2.test_raises_if_person2_not_in_network()

        self.t3.test_person_name_unchanged()
        self.t3.test_person_received_is_same_as_given()
        self.t3.test_raises_if_name_not_exists()
        self.t3.test_test_raises_if_name_is_null()

        self.t4.test_list_contains_friends_of_friends_of_p1()
        self.t4.test_list_contains_friends_of_friends_of_p2()
        self.t4.test_list_contains_friends_of_friends_of_p3()
        self.t4.test_list_contains_friends_of_friends_of_p4()
        # self.t4.test_raises_if_name_is_null()
        # self.t4.test_raises_if_name_not_in_network()


# noinspection PyBroadException
class TestAddPersonProperty(object):
    def __init__(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()

    def setup(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()
        self.n.add_person_property(self.p1, 'name', 'Zach')
        self.n.add_person_property(self.p2, 'name', 'Erin')

    def test_property_is_overwritten(self):
        # asserts that the new property value overwrites the old value
        try:
            self.setup()
            self.n.add_person_property(self.p1, 'tall', False)
            self.n.add_person_property(self.p1, 'tall', True)
            assert self.p1.property['tall'] == True
        except:
            assert False

    def test_raises_if_person_not_in_network(self):
        # asserts that RuntimeError is raised if the given person is not found in the Network
        try:
            self.setup()
            temp = impl.Network()
            p = temp.create_person()
            p.id = -1
            self.n.add_person_property(p, 'name', 'Fred')
        except RuntimeError:
            assert True
        except:
            assert False

    def test_raises_if_name_already_in_network(self):
        # asserts that RuntimeError is raised if a person with given name is already in the Network
        try:
            self.setup()
            self.n.add_person_property(self.p3, 'name', 'Zach')
        except RuntimeError:
            assert True
        except:
            assert False

    # noinspection PyTypeChecker
    def test_raises_if_given_person_is_null(self):
        # asserts that RuntimeError is raised if the given person is None
        try:
            self.setup()
            self.n.add_person_property(None, 'age', 30)
            assert False
        except RuntimeError:
            assert True
        except:
            assert False


# noinspection PyBroadException
class TestAddRelation(object):
    def __init__(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()

    def setup(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()
        self.n.add_person_property(self.p1, 'name', 'Zach')
        self.n.add_person_property(self.p2, 'name', 'Erin')

    def test_raises_if_relation_already_exists(self):
        # asserts that a RuntimeError is thrown if a relationship already exists between the two people
        try:
            self.setup()
            self.n.add_relation(self.p1, self.p2)
            # self.n.add_relation(self.p1, self.p2)
            self.n.add_relation(self.p2, self.p1)
        except RuntimeError:
            assert True
        except:
            assert False

    def test_relation_is_added_if_person1_equals_person2(self):
        # asserts that a relation is added between a person and himself
        try:
            self.setup()
            r = self.n.add_relation(self.p1, self.p1)
            assert r.person1 is self.p1
            assert r.person2 is self.p1
        except:
            assert False

    def test_relation_is_added_if_person1_not_equals_person2(self):
        # asserts that a relation is added between two different people
        try:
            self.setup()
            r = self.n.add_relation(self.p1, self.p2)
            assert r.person1 is self.p1
            assert r.person2 is self.p2
        except:
            assert False

    def test_raises_if_person1_not_exists(self):
        # asserts that a RuntimeError is raised if person1 is not in the network
        try:
            self.setup()
            tempNetwork = impl.Network()
            p = tempNetwork.create_person()
            p.id = -1
            self.n.add_relation(p, self.p2)
            assert False
        except RuntimeError:
            assert True
        except:
            assert False

    def test_raises_if_person2_not_exists(self):
        # asserts that a RuntimeError is raised if person2 is not in the network
        try:
            self.setup()
            tempNetwork = impl.Network()
            p = tempNetwork.create_person()
            p.id = -1
            self.n.add_relation(self.p1, p)
            assert False
        except RuntimeError:
            assert True
        except:
            assert False


# noinspection PyBroadException
class TestAddRelationProperty(object):
    def __init__(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()
        self.r1 = self.n.add_relation(self.p1, self.p2)
        self.r2 = self.n.add_relation(self.p2, self.p3)
        self.r3 = self.n.add_relation(self.p3, self.p3)

    def setup(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()
        self.n.add_person_property(self.p1, 'name', 'Zach')
        self.n.add_person_property(self.p2, 'name', 'Erin')
        self.r1 = self.n.add_relation(self.p1, self.p2)
        self.r2 = self.n.add_relation(self.p2, self.p3)
        self.r3 = self.n.add_relation(self.p3, self.p3)

    def test_property_added_if_person1_equals_person2(self):
        # asserts that a relation property is added between a person and himself
        try:
            self.setup()
            self.n.add_relation_property(self.p3, self.p3, 'foo', 'bar')
            assert self.r3.property['foo'] == 'bar'
        except:
            assert False

    def test_property_added_if_person1_not_equals_person2(self):
        # asserts that a relation property is added between two different people
        try:
            self.setup()
            self.n.add_relation_property(self.p1, self.p2, 'foo', 'bar')
            assert self.r1.property['foo'] == 'bar'
        except:
            assert False

    def test_raises_if_person1_not_in_network(self):
        # asserts that a RuntimeError is thrown if the first person is not in the network
        try:
            self.setup()
            self.n.add_relation_property(self.n.create_person(), self.p2, 'enemy', True)
        except RuntimeError:
            assert True
        except:
            assert False

    def test_raises_if_person2_not_in_network(self):
        # asserts that a RuntimeError is thrown if the second person is not in the network
        try:
            self.setup()
            self.n.add_relation_property(self.p1, self.n.create_person(), 'enemy', True)
        except RuntimeError:
            assert True
        except:
            assert False

    def test_property_value_gets_overwritten(self):
        # asserts that if the given property already exists, then its value is overwritten with the new value
        try:
            self.setup()
            self.n.add_relation_property(self.p1, self.p2, 'enemy', True)
            self.n.add_relation_property(self.p1, self.p2, 'enemy', False)
            assert self.r1.property['enemy'] == False
        except:
            assert False


# noinspection PyBroadException
class TestGetPerson(object):
    def __init__(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()

    def setup(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.n.add_person_property(self.p1, 'name', 'foo')
        self.n.add_person_property(self.p2, 'name', 'bar')

    def test_raises_if_name_not_exists(self):
        # asserts that RuntimeError is raised if the given name is not in the network
        try:
            self.setup()
            self.n.get_person('baz')
            assert False
        except RuntimeError:
            assert True

    def test_test_raises_if_name_is_null(self):
        # asserts that RuntimeError is raised if the given name is None
        try:
            self.setup()
            self.n.get_person(None)
            assert False
        except RuntimeError:
            assert True

    def test_person_name_unchanged(self):
        # test that the name of the person received is the same as the name asked for
        try:
            self.setup()
            p = self.n.get_person('foo')
            assert p.property['name'] == 'foo'
        except:
            assert False

    def test_person_received_is_same_as_given(self):
        # assert that the person received is the same person that was stored
        try:
            self.setup()
            p = self.n.get_person('foo')
            assert p is self.p1
        except:
            assert False


# noinspection PyBroadException
class TestFriendsOfFriends(object):
    def __init__(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()
        self.p4 = self.n.create_person()

    def setup(self):
        self.n = impl.Network()
        self.p1 = self.n.create_person()
        self.p2 = self.n.create_person()
        self.p3 = self.n.create_person()
        self.p4 = self.n.create_person()
        self.n.add_person_property(self.p1, 'name', 'p1')
        self.n.add_person_property(self.p2, 'name', 'p2')
        self.n.add_person_property(self.p3, 'name', 'p3')
        self.n.add_person_property(self.p4, 'name', 'p4')

        # p1 is friends with p2, p3, p4
        self.n.add_relation(self.p1, self.p2)
        self.n.add_relation_property(self.p1, self.p2, 'friend', True)
        self.n.add_relation(self.p1, self.p3)
        self.n.add_relation_property(self.p1, self.p3, 'friend', True)
        self.n.add_relation(self.p1, self.p4)
        self.n.add_relation_property(self.p1, self.p4, 'friend', True)

        # p2 is friends with p1, p3
        # self.n.add_relation(self.p2, self.p1)
        # self.n.add_relation_property(self.p2, self.p1, 'friend', True)
        self.n.add_relation(self.p2, self.p3)
        self.n.add_relation_property(self.p2, self.p3, 'friend', True)

        # p3 is friends with p1, p2
        # self.n.add_relation(self.p3, self.p1)
        # self.n.add_relation_property(self.p3, self.p1, 'friend', True)
        # self.n.add_relation(self.p3, self.p2)
        # self.n.add_relation_property(self.p3, self.p2, 'friend', True)

        # p4 is friends with p1
        # self.n.add_relation(self.p4, self.p1)
        # self.n.add_relation_property(self.p4, self.p1, 'friend', True)

    def test_raises_if_name_not_in_network(self):
        # test that RuntimeError is raised if given name not in network
        try:
            self.setup()
            self.n.friends_of_friends('p5')
            assert False
        except RuntimeError:
            assert True

    def test_raises_if_name_is_null(self):
        # test that RuntimeError is raised if given name is null
        try:
            self.setup()
            self.n.friends_of_friends(None)
            assert False
        except RuntimeError:
            assert True

    def test_list_contains_friends_of_friends_of_p1(self):
        # test only friends of friends of person p1 are returned
        try:
            self.setup()
            friends = self.n.friends_of_friends('p1')
            assert self.p1 in friends
            assert self.p2 in friends
            assert self.p3 in friends
            assert self.p4 not in friends
        except:
            assert False

    def test_list_contains_friends_of_friends_of_p2(self):
        # test only friends of friends of person p2 are returned
        try:
            self.setup()
            friends = self.n.friends_of_friends('p2')
            assert self.p1 in friends
            assert self.p2 in friends
            assert self.p3 in friends
            assert self.p4 in friends
        except:
            assert False

    def test_list_contains_friends_of_friends_of_p3(self):
        # test only friends of friends of person p3 are returned
        try:
            self.setup()
            friends = self.n.friends_of_friends('p3')
            assert self.p1 in friends
            assert self.p2 in friends
            assert self.p3 in friends
            assert self.p4 in friends
        except:
            assert False

    def test_list_contains_friends_of_friends_of_p4(self):
        # test only friends of friends of person p4 are returned
        try:
            self.setup()
            friends = self.n.friends_of_friends('p4')
            assert self.p2 in friends
            assert self.p3 in friends
            assert self.p4 in friends
            assert self.p1 not in friends
        except:
            assert False


if __name__ == '__main__':
    n = TestNetwork()
    # noinspection PyBroadException
    try:
        n.execute()
        print("no error")
    except:
        print("error")