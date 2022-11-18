import numpy
import pystare
import unittest


class MainTest(unittest.TestCase):

    def test_fromlatlon(self):
        lat = numpy.array([30, 45, 60], dtype=numpy.double)
        lon = numpy.array([45, 60, 10], dtype=numpy.double)
        indices = pystare.from_latlon(lat, lon, 12)
        expected = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        numpy.testing.assert_array_equal(indices, expected)

    def test_intervals(self):
        a = numpy.array(
            [0x0000000000000008, 0x000030000000000a, 0x000067ffffffffff, 0x000070000000000a, 0x0000907fffffffff],
            dtype=numpy.int64)
        starts, ends = pystare.from_intervals(a)
        self.assertEqual(starts[0], 8)
        self.assertEqual(ends[0], 8796093022207)

    def test_tolatlon(self):
        indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        lat, lon = pystare.to_latlon(indices)
        numpy.testing.assert_allclose(lat, numpy.array([30, 45, 60]), verbose=True)
        numpy.testing.assert_allclose(lon, numpy.array([45, 60, 10]), verbose=True)

    def test_tolatlonlevel(self):
        indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        lat, lon, level = pystare.to_latlonlevel(indices)
        numpy.testing.assert_allclose(lat, numpy.array([30, 45, 60]), verbose=True)
        numpy.testing.assert_allclose(lat, numpy.array([30, 45, 60]), verbose=True)
        numpy.testing.assert_allclose(level, numpy.array([12, 12, 12]), verbose=True)

    def test_latlonroundtrip(self):
        lat1 = numpy.array([30, 45, 60], dtype=numpy.double)
        lon1 = numpy.array([45, 60, 10], dtype=numpy.double)
        level1 = 12
        indices = pystare.from_latlon(lat1, lon1, level1)
        lat2, lon2, level2 = pystare.to_latlonlevel(indices)
        numpy.testing.assert_allclose(lat1, lat2)
        numpy.testing.assert_allclose(lon1, lon2)
        self.assertEqual(level1, level2[0])

    def test_tolevel(self):
        indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        level = pystare.to_level(indices)
        numpy.testing.assert_array_equal(level, numpy.array([12, 12, 12]), verbose=True)

    def test_toarea(self):
        indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        area = pystare.to_area(indices)
        expected = numpy.array([8.66507750e-08, 8.74786654e-08, 7.97819113e-08])
        numpy.testing.assert_allclose(area, expected)

    def test__tocompressedrange(self):

        # indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        # expected = numpy.array([3643626718498217164, 4151504989081014892, 4161865161846704588])

        indices = numpy.array([0x399d1bcabd6f926c, 0x39c1ea506ef249cc, 0x3290c3321a355ccc])
        expected = numpy.array([0x3290c3300000000c, 0x399d1bc80000000c, 0x39c1ea500000000c])

        compressed = numpy.array([0, 0, 0], dtype=numpy.int64)
        pystare.core._to_compressed_range(indices, compressed)

        numpy.testing.assert_array_equal(compressed, expected)

    def test_tocompressedrange(self):

        # indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        # expected = numpy.array([3643626718498217164, 4151504989081014892, 4161865161846704588])

        indices = numpy.array([0x399d1bcabd6f926c, 0x39c1ea506ef249cc, 0x3290c3321a355ccc])
        expected = numpy.array([0x3290c3300000000c, 0x399d1bc80000000c, 0x39c1ea500000000c])

        compressed = pystare.to_compressed_range(indices)

        # print('')
        # print('indices','compressed','expected')
        # for i in [0,1,2]:
        #     print(i,hex(indices[i]),hex(compressed[i]),hex(expected[i]))
        # print('\nindices')
        # for i in [0,1,2]:
        #     print(hex(indices[i]))
        # print('\ncompressed')
        # for i in [0,1,2]:
        #     print(hex(compressed[i]))

        numpy.testing.assert_array_equal(compressed, expected)

    def test__tohullrange(self):
        indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        result_size = numpy.zeros([1], dtype=numpy.int64)
        result = pystare.core._to_hull_range(indices, 8)
        hull_indices = numpy.zeros([result.get_size_as_intervals()], dtype=numpy.int64)
        result.copy_as_intervals(hull_indices)
        self.assertEqual(hull_indices.size, 901)

    def test_tohullrange(self):
        indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        hull_indices = pystare.to_hull_range(indices, 8)
        self.assertEqual(hull_indices.size, 901)

    def test__cmpspatial(self):
        indices = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        compared = numpy.zeros([9], dtype=numpy.int64)
        pystare.core._cmp_spatial(indices, indices, compared)
        expected = numpy.array([1, 0, 0, 0, 1, 0, 0, 0, 1])
        numpy.testing.assert_array_equal(compared, expected)

    def test_cmpspatial(self):
        indices1 = numpy.array([4151504989081014892, 4161865161846704588, 3643626718498217164])
        indices2 = numpy.zeros([2], dtype=numpy.int64)
        indices2[0] = indices1[1] - 2
        indices2[1] = indices1[1]
        compared = pystare.cmp_spatial(indices1, indices2)
        expected = numpy.array([0, 0, -1, 1, 0, 0])
        numpy.testing.assert_array_equal(compared, expected)

    def test__expand(self):
        import tests.data.intervals as intervals
        src = numpy.array(intervals.src, dtype=numpy.int64)
        expected_expanded = numpy.array(intervals.expanded_src, dtype=numpy.int64)
        expanded = numpy.zeros([len(expected_expanded)], dtype=numpy.int64)
        expanded_len = numpy.zeros([1], dtype=numpy.int64)
        intervals_len = len(src)
        resolution = -1
        result = pystare.core._expand_intervals(src, resolution, multi_resolution=False)
        expanded_len = result.get_size_as_values()
        result.copy_as_values(expanded)
        self.assertEqual(expanded_len, 74)
        error_found = False
        for i in range(len(expanded)):
            if expanded[i] != expected_expanded[i]:
                error_found = True
        self.assertFalse(error_found)

    def test_expand(self):
        import tests.data.intervals as intervals
        src = numpy.array(intervals.src, dtype=numpy.int64)
        expected_expanded = numpy.array(intervals.expanded_src, dtype=numpy.int64)
        resolution = -1
        expanded = pystare.expand_intervals(src, resolution, multi_resolution=False)
        error_found = False
        for i in range(len(expanded)):
            if expanded[i] != expected_expanded[i]:
                error_found = True
        self.assertFalse(error_found)

    def test_cover(self):
        expected = [(0, 4430603050402447369),
                    (295, 4430595237856935950),
                    (590, 4430626891765907470),
                    (885, 4430691958372958222),
                    (1180, 4430869121478950926)]
        cover = pystare.latlon2circular_cover(1.5, 0.5, 0.25, 14)
        for i in list(expected):
            self.assertEqual(i[1], cover[i[0]])

    def test_spatial_resolution_from_km(self):
        self.assertEqual(10, int(pystare.spatial_resolution_from_km(10)))

    def test_spatial_resolution(self):
        self.assertEqual(11, int(pystare.spatial_resolution(11)))
        self.assertEqual(15, int(pystare.spatial_resolution(15)))
