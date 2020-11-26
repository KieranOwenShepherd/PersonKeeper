import unittest
import os
from persons import Record, Records

class TestAddRemove(unittest.TestCase):
    def setUp(self):
        self.recs = Records()
        self.rec_santa = Record(name="Nicholas",address="23 North Pole Road",phone=247478627)

    def test_add(self):
        self.assertEqual(tuple(self.recs),tuple())
        self.recs.add_record(self.rec_santa)
        self.assertEqual(tuple(self.recs),(self.rec_santa,))

    def test_init(self):
       self.assertEqual( tuple(Records([self.rec_santa])), (self.rec_santa,) )
    

class TestUpdateFilter(unittest.TestCase):
    def setUp(self):
        self.rec_santa = Record(name="Nicholas",address="23 North Pole Road",phone=247478627)
        self.rec_edw = Record(name="Edward",address="1774 Tinsmith Cir",phone=724776742637)
        self.rec_paul = Record(name="Paul",address="55 North Road",phone=2767853)
        self.recs = Records([self.rec_santa, self.rec_edw, self.rec_paul])

    def test_update(self):
        with self.assertRaises(KeyError):
            self.recs.update_record('000', Record(name='test', address='test',phone='test'))

    def test_filter(self):
        self.assertEqual(tuple(self.recs.filter_records()), tuple(self.recs))
        self.assertEqual(tuple(self.recs.filter_records(phone='*47*')), (self.rec_santa, self.rec_edw))
        self.assertEqual(tuple(self.recs.filter_records(address='*North*')), (self.rec_santa, self.rec_paul))
        self.assertEqual(tuple(self.recs.filter_records(phone='*47*', address='*North*')), (self.rec_santa,))


class TestLoadExport(unittest.TestCase):
    def setUp(self):
        # A better location may need to be chosen
        self.csv_file = os.path.join(os.path.split(__file__)[0],"testdb.csv")
        self.rec_santa = Record(name="Nicholas",address="23 North Pole Road",phone=247478627)
        self.recd = Record("Joe","22 something court",4012334)
        with open(self.csv_file,'w+') as f:
            f.write(",name,address,phone\na8cd0b5c-eab0-417f-82ec-8a6c4bc15fa5,Joe,22 something court,4012334")

    def tearDown(self):
        os.remove(self.csv_file)

    def test_loadfile(self):
        with self.assertRaises(ValueError):
            Records.from_file('testfile.jpg') # jpg is not supported

        records = Records.from_file(self.csv_file)
        self.assertEqual(tuple(records), (self.recd,))

        records.add_record(self.rec_santa)
        records.export(self.csv_file) #just verify that it doesn't error
        
        with self.assertRaises(ValueError):
            records.export('testfile.jpg') # jpg is not supported


if __name__ == '__main__':
    unittest.main()
