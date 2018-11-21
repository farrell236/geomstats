"""
Unit tests for Stiefel manifolds.
"""

import unittest
import warnings

import geomstats.backend as gs
import tests.helper as helper

from geomstats.stiefel import Stiefel

ATOL = 1e-6


class TestStiefelMethods(unittest.TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        """
        Tangent vectors constructed following:
        http://noodle.med.yale.edu/hdtag/notes/steifel_notes.pdf
        """
        warnings.simplefilter('ignore', category=ImportWarning)

        gs.random.seed(1234)

        self.p = 3
        self.n = 4
        self.space = Stiefel(self.n, self.p)
        self.n_samples = 10
        self.dimension = int(
            self.p * self.n - (self.p * (self.p + 1) / 2))

        self.point_a = gs.array([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.],
            [0., 0., 0.]])

        self.point_b = gs.array([
            [1. / gs.sqrt(2), 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.],
            [1. / gs.sqrt(2), 0., 0.]])

        point_perp = gs.array([
            [0.],
            [0.],
            [0.],
            [1.]])

        matrix_a_1 = gs.array([
            [0., 2., -5.],
            [-2., 0., -1.],
            [5., 1., 0.]])

        matrix_b_1 = gs.array([
            [-2., 1., 4.]])

        matrix_a_2 = gs.array([
            [0., 2., -5.],
            [-2., 0., -1.],
            [5., 1., 0.]])

        matrix_b_2 = gs.array([
            [-2., 1., 4.]])

        self.tangent_vector_1 = (
            gs.matmul(self.point_a, matrix_a_1)
            + gs.matmul(point_perp, matrix_b_1))

        self.tangent_vector_2 = (
            gs.matmul(self.point_a, matrix_a_2)
            + gs.matmul(point_perp, matrix_b_2))

        self.metric = self.space.euclidean_metric

    def test_belongs(self):
        point = self.space.random_uniform()
        belongs = self.space.belongs(point)

        gs.testing.assert_allclose(belongs.shape, (1, 1))

    def test_random_and_belongs(self):
        point = self.space.random_uniform()
        result = self.space.belongs(point)
        expected = gs.array([[True]])

        gs.testing.assert_allclose(result, expected)

    def test_random_uniform(self):
        point = self.space.random_uniform()

        gs.testing.assert_allclose(point.shape, (1, self.n, self.p))

    def test_inner_product(self):
        base_point = self.point_a

        result = self.metric.inner_product(
            self.tangent_vector_1,
            self.tangent_vector_2,
            base_point=base_point)

        expected = gs.trace(
            gs.matmul(
                self.tangent_vector_1.T,
                self.tangent_vector_2))

        gs.testing.assert_allclose(result, expected)

    def test_log_and_exp_general_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.
        """
        # Riemannian Log then Riemannian Exp
        # General case
        base_point = self.point_a
        point = self.point_b

        log = self.metric.log(point=point, base_point=base_point)
        result = self.metric.exp(tangent_vec=log, base_point=base_point)
        expected = helper.to_matrix(point)

        gs.testing.assert_allclose(result, expected, atol=ATOL)


if __name__ == '__main__':
        unittest.main()
