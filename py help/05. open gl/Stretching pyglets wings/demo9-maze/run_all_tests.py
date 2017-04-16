#! python

from unittest import makeSuite, TestSuite, TextTestRunner

from test.room_test import Room_test
from test.vertexutils_test import Vertexutils_test

suite = TestSuite()
suite.addTests(makeSuite(Room_test,'test'))
suite.addTests(makeSuite(Vertexutils_test,'test'))

runner = TextTestRunner()
runner.run(suite)

