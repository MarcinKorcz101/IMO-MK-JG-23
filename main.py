from lab1.GreedyAlgorithms import GreedyAlgorithms

if __name__ == '__main__':
    ga = GreedyAlgorithms('lab1/kroa100.tsp')
    ga.read()
    ga.run('nearest neighbour') # specify method - one of [nearest neighbour, cycle, regret]
    # ga.run('cycle')
