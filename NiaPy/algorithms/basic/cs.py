# encoding=utf8
# pylint: disable=mixed-indentation, line-too-long, singleton-comparison, multiple-statements, attribute-defined-outside-init, no-self-use, logging-not-lazy, unused-variable, arguments-differ, bad-continuation
import logging
from numpy import apply_along_axis, argsort, inf
from scipy.stats import levy
from NiaPy.algorithms.algorithm import Algorithm

logging.basicConfig()
logger = logging.getLogger('NiaPy.algorithms.basic')
logger.setLevel('INFO')

__all__ = ['CuckooSearch']

class CuckooSearch(Algorithm):
	r"""Implementation of Cuckoo behaviour and levy flights.

	**Algorithm:** Cuckoo Search

	**Date:** 2018

	**Authors:** Klemen Berkovič

	**License:** MIT

	**Reference:** Yang, Xin-She, and Suash Deb. "Cuckoo search via Lévy flights." Nature & Biologically Inspired Computing, 2009. NaBIC 2009. World Congress on. IEEE, 2009.
	"""
	Name = ['CuckooSearch', 'CS']
	N, pa, alpha = 50, 0.2, 0.5

	@staticmethod
	def typeParameters(): return {
		'N': lambda x: isinstance(x, int) and x > 0,
		'pa': lambda x: isinstance(x, float) and 0 <= x <= 1,
		'alpha': lambda x: isinstance(x, (float, int)),
	}

	def setParameters(self, N=50, pa=0.2, alpha=0.5, **ukwargs):
		r"""Set the arguments of an algorithm.

		**Arguments:**
		N {integer} -- population size $\in [1, \infty)$
		pa {real} -- factor $\in [0, 1]$
		"""
		self.N, self.pa, self.alpha = N, pa, alpha
		if ukwargs: logger.info('Unused arguments: %s' % (ukwargs))

	def emptyNests(self, pop, fpop, pa_v, task):
		si = argsort(fpop)[:int(pa_v):-1]
		pop[si] = task.Lower + self.rand(task.D) * task.bRange
		fpop[si] = apply_along_axis(task.eval, 1, pop[si])
		return pop, fpop

	def initPopulation(self, task):
		pa_v = self.N * self.pa
		N = task.Lower + self.rand([self.N, task.D]) * task.bRange
		N_f = apply_along_axis(task.eval, 1, N)
		return N, N_f, {'pa_v': pa_v}

	def runIteration(self, task, pop, fpop, xb, fxb, pa_v, **dparams):
		i = self.randint(self.N)
		Nn = task.repair(pop[i] + self.alpha * levy.rvs(size=[task.D], random_state=self.Rand), rnd=self.Rand)
		Nn_f = task.eval(Nn)
		j = self.randint(self.N)
		while i == j: j = self.randint(self.N)
		if Nn_f <= fpop[j]: pop[j], fpop[j] = Nn, Nn_f
		pop, fpop = self.emptyNests(pop, fpop, pa_v, task)
		return pop, fpop, {'pa_v': pa_v}

# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
