# -*- coding: utf-8 -*-
import numpy as np
import unittest
from skimage import data

from .. import mnxc2

np.random.seed(23)
    
class TestMNXC2(unittest.TestCase):

	def test_trivial(self):
		""" Test that the autocorrelation using mnxc2 has a single
		peak of 1 """
		im = np.random.random(size = (32,32))
		im2 = np.random.random(size = (32,32))

		xcorr = mnxc2(im, im2)
		self.assertGreaterEqual(xcorr.min(), -1)
		self.assertLessEqual(xcorr.max(), 1)
	
	def test_side_effects(self):
		""" Test that mnxc2 does not modify the input in-place """
		im1 = np.random.random(size = (32,32))
		im2 = np.random.random(size = (32,32))

		m1 = np.random.choice([True, False], size = im1.shape)
		m2 = np.random.choice([True, False], size = im2.shape)

		# If arrays are written to, ValueError is raised
		for arr in (im1, im2, m1, m2):
			arr.setflags(write = False)
		
		xcorr = mnxc2(im1, im2, m1, m2)
	
	def test_range(self):
		im = np.random.random(size = (128,32))
		im2 = np.random.random(size = (128,32))

		m1 = np.random.choice([True, False], size = im.shape)
		m2 = np.random.choice([True, False], size = im2.shape)

		xcorr = mnxc2(im, im2, m1, m2).real
		self.assertGreaterEqual(xcorr.min(), -1)
		self.assertLessEqual(xcorr.max(), 1)


if __name__ == '__main__':
	unittest.main()