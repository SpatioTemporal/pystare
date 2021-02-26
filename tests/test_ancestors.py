import numpy 
import pystare 
import unittest

class MainTest(unittest.TestCase):
    
    def test_parent(self):
        sid = 0x300a30000000000a
        parent = pystare.parent(sid)
        self.assertEqual('0x300a300000000009', parent)
    
    def test_children(self):
        sid = 0x300a300000000009
        children1 = [0x300a30000000000a, 0x300a30800000000a, 0x300a31000000000a, 0x300a31800000000a]
        children2 = pystare.children(sid)
        with self.subTest():
            self.assertEqual(children2.size, 4)
        with self.subTest():    
            self.assertTrue(set(list(children1)), set(children1))
            
    def test_is_ancestor(self):
        is_ancestor = pystare.is_ancestor(0x300a30000000000a, 0x300a300000000009)
        self.assertTrue(is_ancestor)
        
        
