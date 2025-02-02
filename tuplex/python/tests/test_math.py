#!/usr/bin/env python3
#----------------------------------------------------------------------------------------------------------------------#
#                                                                                                                      #
#                                       Tuplex: Blazing Fast Python Data Science                                       #
#                                                                                                                      #
#                                                                                                                      #
#  (c) 2017 - 2021, Tuplex team                                                                                        #
#  Created by Leonhard Spiegelberg first on 1/1/2021                                                                   #
#  License: Apache 2.0                                                                                                 #
#----------------------------------------------------------------------------------------------------------------------#

import unittest
import tuplex
from helper import test_options


# different flavors of imports...
from math import pi
import math


class TestMath(unittest.TestCase):

    def setUp(self):
        self.conf = test_options()

    def test_constants(self):
        c = tuplex.Context(test_options())

        # Note that in order to extract this, we need to put lambdas on separate lines...
        res = c.parallelize([0]).map(lambda x: (pi, math.e, math.tau, math.inf, math.nan, -math.inf)) \
            .map(lambda a,b,c,d,e,f: (str(a), str(b), str(c), str(d), str(e), str(f))).collect()

        self.assertEqual(res, [('3.14159', '2.71828', '6.28319', 'inf', 'nan', '-inf')])

    def testLog(self):
        c = tuplex.Context(self.conf)

        test = [math.e, 1.0, math.e ** 2, math.e ** -1]
        L1 = c.parallelize(test).map(lambda x: math.log(x)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], 1.0)
        self.assertAlmostEqual(L1[1], 0.0)
        self.assertAlmostEqual(L1[2], 2.0)
        self.assertAlmostEqual(L1[3], -1.0)

        int_test = [3, 1, 2, 6]
        L2 = c.parallelize(int_test).map(lambda x: math.log(x)).collect()
        assert len(L2) == 4, 'wrong length'
        self.assertAlmostEqual(L2[0], math.log(3))
        self.assertAlmostEqual(L2[1], 0.0)
        self.assertAlmostEqual(L2[2], math.log(2))
        self.assertAlmostEqual(L2[3], math.log(6))

        bool_test = [True, False]
        L_bool = c.parallelize(bool_test).map(lambda x: math.log(x)).collect()
        assert len(L_bool) == 2
        self.assertAlmostEqual(L_bool[0], 0.0)
        self.assertAlmostEqual(L_bool[1], -math.inf)


    def testExp(self):
        c = tuplex.Context(self.conf)

        test = [1.0, 0.0, 2.0, -1.0]
        L1 = c.parallelize(test).map(lambda x: math.exp(x)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], math.e)
        self.assertAlmostEqual(L1[1], math.exp(0.0))
        self.assertAlmostEqual(L1[2], math.exp(2.0))
        self.assertAlmostEqual(L1[3], math.exp(-1.0))

        int_test = [0, 1, -1, 4, -4]
        L2 = c.parallelize(int_test).map(lambda x: math.exp(x)).collect()
        assert len(L2) == 5, 'wrong length'
        self.assertAlmostEqual(L2[0], 1.0)
        self.assertAlmostEqual(L2[1], math.e)
        self.assertAlmostEqual(L2[2], math.exp(-1))
        self.assertAlmostEqual(L2[3], math.exp(4))
        self.assertAlmostEqual(L2[4], math.exp(-4))

        bool_test = [True, False]
        L_bool = c.parallelize(bool_test).map(lambda x: math.exp(x)).collect()
        assert len(L_bool) == 2
        assert L_bool[0] == math.exp(True)
        assert L_bool[1] == math.exp(False)


    def testSin(self):
        c = tuplex.Context(self.conf)

        test = [0.0, math.pi/2, -math.pi/2]
        L1 = c.parallelize(test).map(lambda x: math.sin(x)).collect()
        assert L1 == [0, 1, -1]

    def testSinH(self):
        c = tuplex.Context(self.conf)

        test = [0.0]
        L1 = c.parallelize(test).map(lambda x: math.sinh(x)).collect()
        assert L1 == [0]

    def testArcSin(self):
        c = tuplex.Context(self.conf)

        test = [-1.0, 0.0, 1.0]
        L1 = c.parallelize(test).map(lambda x: math.asin(x)).collect()
        assert L1 == [-math.pi/2, 0, math.pi/2]

    def testArcSinH(self):
        c = tuplex.Context(self.conf)

        test = [0.0, 1.0, -1.0]
        L1 = c.parallelize(test).map(lambda x: math.asinh(x)).collect()
        assert L1 == [0, 0.88137358701954305, -0.88137358701954305]

    def testCos(self):
        c = tuplex.Context(self.conf)

        test = [-math.pi/2, 0.0, math.pi/2, math.pi]
        L1 = c.parallelize(test).map(lambda x: math.cos(x)).collect()
        L1[0] = round(L1[0], 6)
        L1[2] = round(L1[2], 6)
        assert L1 == [0, 1, 0, -1]

    def testCosH(self):
        c = tuplex.Context(self.conf)

        test = [0.0]
        L1 = c.parallelize(test).map(lambda x: math.cosh(x)).collect()
        assert L1 == [1]

    def testArcCos(self):
        c = tuplex.Context(self.conf)

        test = [-1.0, 0.0, 1.0]
        L1 = c.parallelize(test).map(lambda x: math.acos(x)).collect()
        assert L1 == [math.pi, math.pi/2, 0]

    def testArcCosH(self):
        c = tuplex.Context(self.conf)

        test = [1.0, 2.0]
        L1 = c.parallelize(test).map(lambda x: math.acosh(x)).collect()
        L1 = [round(x, 5) for x in L1]
        assert L1 == [0, 1.31696]

    def testTanH(self):
        c = tuplex.Context(self.conf)

        test = [0.0, float("inf"), float("-inf")]
        L1 = c.parallelize(test).map(lambda x: math.tanh(x)).collect()
        assert L1 == [0, 1, -1]

    def testArcTan(self):
        c = tuplex.Context(self.conf)

        test = [-1.0, 0.0, 1.0, float('inf'), float('-inf')]
        L1 = c.parallelize(test).map(lambda x: math.atan(x)).collect()
        assert L1 == [-math.pi/4, 0, math.pi/4, math.pi/2, -math.pi/2]

    def testArcTan2(self):
        c = tuplex.Context(self.conf)

        test = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]
        L1 = c.parallelize(test).map(lambda x, y: math.atan2(x, y)).collect()
        assert L1 == [-math.pi/2, -math.pi/4, 0, math.pi/4, math.pi/2]

    def testArcTanH(self):
        c = tuplex.Context(self.conf)

        test = [0.0, 0.5, -0.5]
        L1 = c.parallelize(test).map(lambda x: math.atanh(x)).collect()
        assert math.isclose(L1[0], 0)
        assert math.isclose(L1[1], 0.5493061443340549)
        assert math.isclose(L1[2], -0.5493061443340549)

    def testToRadians(self):
        c = tuplex.Context(self.conf)

        test = [180.0, 90.0, -45.0, 0.0]
        L1 = c.parallelize(test).map(lambda x: math.radians(x)).collect()
        assert L1 == [math.pi, math.pi/2, -math.pi/4, 0]

    def testToDegrees(self):
        c = tuplex.Context(self.conf)

        test = [math.pi, math.pi/2, -math.pi/4, 0.0]
        L1 = c.parallelize(test).map(lambda x: math.degrees(x)).collect()
        assert L1 == [180, 90, -45, 0]

    def testSquareRoot(self):
        c = tuplex.Context(self.conf)

        test = [0.0, 1.0, 4.0]
        L1 = c.parallelize(test).map(lambda x: math.sqrt(x)).collect()
        assert L1 == [0, 1, 2]

    def testLog1p(self):
        c = tuplex.Context(self.conf)

        test = [math.e - 1, math.e ** 2 - 1, math.e ** -1 - 1]
        L1 = c.parallelize(test).map(lambda x: math.log1p(x)).collect()
        assert len(L1) == 3, 'wrong length'
        self.assertAlmostEqual(L1[0], 1.0)
        self.assertAlmostEqual(L1[1], 2.0)
        self.assertAlmostEqual(L1[2], -1.0)

        int_test = [0, 1, 4]
        L2 = c.parallelize(int_test).map(lambda x: math.log1p(x)).collect()
        assert len(L2) == 3, 'wrong length'
        self.assertAlmostEqual(L2[0], 0.0)
        self.assertAlmostEqual(L2[1], math.log1p(1))
        self.assertAlmostEqual(L2[2], math.log1p(4))

        bool_test = [True, False]
        L_bool = c.parallelize(bool_test).map(lambda x: math.log1p(x)).collect()
        assert len(L_bool) == 2
        assert L_bool[0] == math.log1p(True)
        assert L_bool[1] == math.log1p(False)


    def testLog2(self):
        c = tuplex.Context(self.conf)

        test = [2.0, 1.0, 4.0, 1 / 4]
        L1 = c.parallelize(test).map(lambda x: math.log2(x)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], 1.0)
        self.assertAlmostEqual(L1[1], 0.0)
        self.assertAlmostEqual(L1[2], 2.0)
        self.assertAlmostEqual(L1[3], -2.0)

        int_test = [2, 1, 4, 8]
        L2 = c.parallelize(int_test).map(lambda x: math.log2(x)).collect()
        assert len(L2) == 4, 'wrong length'
        self.assertAlmostEqual(L2[0], 1.0)
        self.assertAlmostEqual(L2[1], 0.0)
        self.assertAlmostEqual(L2[2], 2.0)
        self.assertAlmostEqual(L2[3], 3.0)

        bool_test = [True, False]
        L_bool = c.parallelize(bool_test).map(lambda x: math.log2(x)).collect()
        assert len(L_bool) == 2
        self.assertAlmostEqual(L_bool[0], 0.0)
        self.assertAlmostEqual(L_bool[1], -math.inf)


    def testLog10(self):
        c = tuplex.Context(self.conf)

        test = [10.0, 1.0, 1000.0, 1 / 10]
        L1 = c.parallelize(test).map(lambda x: math.log10(x)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], 1.0)
        self.assertAlmostEqual(L1[1], 0.0)
        self.assertAlmostEqual(L1[2], 3.0)
        self.assertAlmostEqual(L1[3], -1.0)

        int_test = [10, 1, 100, 1000]
        L2 = c.parallelize(int_test).map(lambda x: math.log10(x)).collect()
        assert len(L2) == 4, 'wrong length'
        self.assertAlmostEqual(L2[0], 1.0)
        self.assertAlmostEqual(L2[1], 0.0)
        self.assertAlmostEqual(L2[2], 2.0)
        self.assertAlmostEqual(L2[3], 3.0)

        bool_test = [True, False]
        L_bool = c.parallelize(bool_test).map(lambda x: math.log10(x)).collect()
        assert len(L_bool) == 2
        self.assertAlmostEqual(L_bool[0], 0.0)
        self.assertAlmostEqual(L_bool[1], -math.inf)


    def testExpm1(self):
        c = tuplex.Context(self.conf)

        test = [-1.0, 1.0,  2.0, 0.0]
        L1 = c.parallelize(test).map(lambda x: math.expm1(x)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], math.expm1(-1.0))
        self.assertAlmostEqual(L1[1], math.expm1(1.0))
        self.assertAlmostEqual(L1[2], math.expm1(2.0))
        self.assertAlmostEqual(L1[3], math.expm1(0.0))


        int_test = [1, -1, 0, 2]
        L2 = c.parallelize(int_test).map(lambda x: math.expm1(x)).collect()
        assert len(L2) == 4, 'wrong length'
        self.assertAlmostEqual(L2[0], math.expm1(1))
        self.assertAlmostEqual(L2[1], math.expm1(-1))
        self.assertAlmostEqual(L2[2], math.expm1(0))
        self.assertAlmostEqual(L2[3], math.expm1(2))

        bool_test = [True, False]
        L_bool = c.parallelize(bool_test).map(lambda x: math.expm1(x)).collect()
        assert len(L_bool) == 2
        assert L_bool[0] == math.expm1(True)
        assert L_bool[1] == math.expm1(False)



    def testPow(self):
        c = tuplex.Context(self.conf)

        test1 = [-1.0, 1.0,  2.0, 0.0]
        L1 = c.parallelize(test1).map(lambda x: math.pow(-3.0, x)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], -1.0 / 3.0)
        self.assertAlmostEqual(L1[1], -3.0)
        self.assertAlmostEqual(L1[2], 9.0)
        self.assertAlmostEqual(L1[3], 1.0)

        test2 = [-1.0, 1.0, 2.0, 0.0]
        L1 = c.parallelize(test2).map(lambda x: math.pow(x, 2.0)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], 1.0)
        self.assertAlmostEqual(L1[1], 1.0)
        self.assertAlmostEqual(L1[2], 4.0)
        self.assertAlmostEqual(L1[3], 0.0)

        test3 = [(-1.0, 4.0), (1.0, -2.0), (2.0, 0.0), (-3.0, 0.0)]
        L1 = c.parallelize(test3).map(lambda x, y: math.pow(x, y)).collect()
        assert len(L1) == 4, 'wrong length'
        self.assertAlmostEqual(L1[0], 1.0)
        self.assertAlmostEqual(L1[1], 1.0)
        self.assertAlmostEqual(L1[2], 1.0)
        self.assertAlmostEqual(L1[3], 1.0)

        int_test1 = [1, -1, 0, 2]
        L2 = c.parallelize(int_test1).map(lambda x: math.pow(2, x)).collect()
        assert len(L2) == 4, 'wrong length'
        self.assertAlmostEqual(L2[0], 2.0)
        self.assertAlmostEqual(L2[1], 0.5)
        self.assertAlmostEqual(L2[2], 1.0)
        self.assertAlmostEqual(L2[3], 4.0)

        int_test2 = [1, -1, -2, 2]
        L3 = c.parallelize(int_test2).map(lambda x: math.pow(x, 0)).collect()
        assert len(L3) == 4, 'wrong length'
        self.assertAlmostEqual(L3[0], 1.0)
        self.assertAlmostEqual(L3[1], 1.0)
        self.assertAlmostEqual(L3[2], 1.0)
        self.assertAlmostEqual(L3[3], 1.0)

        int_test3 = [(1, -2), (-1, 2), (0, 1), (2, -2)]
        L4 = c.parallelize(int_test3).map(lambda x, y: math.pow(x, y)).collect()
        assert len(L4) == 4, 'wrong length'
        self.assertAlmostEqual(L4[0], 1.0)
        self.assertAlmostEqual(L4[1], 1.0)
        self.assertAlmostEqual(L4[2], 0.0)
        self.assertAlmostEqual(L4[3], 0.25)

        bool_test = [(True, False), (True, True), (False, True), (False, False)]
        L_bool = c.parallelize(bool_test).map(lambda x, y: math.pow(x, y)).collect()
        assert len(L_bool) == 4
        assert L_bool[0] == math.pow(True, False)
        assert L_bool[1] == math.pow(True, True)
        assert L_bool[2] == math.pow(False, True)
        assert L_bool[3] == math.pow(False, False)