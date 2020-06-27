from table import *


def test_groupby():
    t = Table()
    for c in 'abcde':
        t.add_column(header=c, datatype=int, allow_empty=False, data=[i for i in range(5)])

    # we want to add two new columns using the functions:
    def f1(a, b, c):
        return a + b + c + 1

    def f2(b, c, d):
        return b * c * d

    # and we want to compute two new columns 'f' and 'g':
    t.add_column(header='f', datatype=int, allow_empty=False)
    t.add_column(header='g', datatype=int, allow_empty=True)

    # we can now use the filter, to iterate over the table:
    for row in t.filter('a', 'b', 'c', 'd'):
        a, b, c, d = row

        # ... and add the values to the two new columns
        t['f'].append(f1(a, b, c))
        t['g'].append(f2(b, c, d))

    assert len(t) == 5
    assert list(t.columns) == list('abcdefg')
    t.show()

    g = GroupBy(keys=['a', 'b'],
                functions=[('f', Max),
                           ('f', Min),
                           ('f', Sum),
                           ('f', First),
                           ('f', Last),
                           ('f', Count),
                           ('f', CountUnique),
                           ('f', Average),
                           ('f', StandardDeviation),
                           ('a', StandardDeviation),
                           ('f', Median),
                           ('f', Mode),
                           ('g', Median)])
    t2 = t + t
    assert len(t2) == 2 * len(t)
    t2.show()

    g += t2

    assert list(g.rows) == [
        (0, 0, 1, 1, 2, 1, 1, 2, 1, 1.0, 0.0, 0.0, 1, 1, 0),
        (1, 1, 4, 4, 8, 4, 4, 2, 1, 4.0, 0.0, 0.0, 4, 4, 1),
        (2, 2, 7, 7, 14, 7, 7, 2, 1, 7.0, 0.0, 0.0, 7, 7, 8),
        (3, 3, 10, 10, 20, 10, 10, 2, 1, 10.0, 0.0, 0.0, 10, 10, 27),
        (4, 4, 13, 13, 26, 13, 13, 2, 1, 13.0, 0.0, 0.0, 13, 13, 64)
    ]

    g.table.show()

    g2 = GroupBy(keys=['a', 'b'], functions=[('f', Max), ('f', Sum)])
    g2 += t + t + t

    g2.table.show()

    pivot_table = g2.pivot(columns=['b'])

    pivot_table.show()