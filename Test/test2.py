from queue import PriorityQueue

class MCNode:
  def __init__(self, m, c, b):
    self.missionaries = m
    self.cannibals = c
    self.boatpos = b
    self.h = (m * m + c * c + 2 * m * c)
    self.predecessor = None

  def __eq__(self, other):
    return other.boatpos == self.boatpos and \
           other.missionaries == self.missionaries and \
           other.cannibals == self.cannibals

  def getAdjacentNodes(self, m, c, bc):
    adj_nodes = []
    carry = 1
    while carry <= bc:
      carrym = carry
      carryc = 0
      while carrym >= 0:
        if self.boatpos == 'L':
          newm = self.missionaries - carrym
          newc = self.cannibals - carryc
          if newm >= 0 and newc >= 0 and (newm >= newc or newm == 0) and ((m - newm) >= (c - newc) or (m - newm == 0)):
            adj_nodes.append(MCNode(newm, newc, 'R'))
        elif self.boatpos == 'R':
          newm = self.missionaries + carrym
          newc = self.cannibals + carryc
          if newm <= m and newc <= c and (newm >= newc or newm == 0) and ((m - newm) >= (c - newc) or (m - newm == 0)):
            adj_nodes.add(MCNode(newm, newc, 'L'))
        carrym -= 1
        carryc += 1
      carry += 1
    return adj_nodes

  def printPath(self):
    if self.predecessor is not None:
      self.predecessor.printPath()
    print("<" + self.missionaries + "," + self.cannibals + "," + self.boatpos + "> ")


class MCGraph:
  def __init__(self):
    self.vertex_list = []
    self.open_list = []
    self.closed_list = []
    self.maxm = 0
    self.maxc = 0
    self.boatcarry = 0

  def astarSearch(self, m, c, bc):
    siddu_steps = 0
    self.maxm = m
    self.maxc = c
    self.boatcarry = bc
    self.open_list = PriorityQueue()
    self.closed_list = set()
    start = MCNode(m, c, 'L')
    start.g = 0
    self.open_list.put((start.h + start.g, start))
    transfer_node = None
    while ( not self.open_list.empty()) and (transfer_node is None or transfer_node.missionaries != 0 or transfer_node.cannibals != 0 or transfer_node.boatpos != 'R'):
      siddu_steps += 1
      transfer_node = self.open_list.get()
      self.closed_list.add(transfer_node)
      adj_nodes = transfer_node.getAdjacentNodes(m, c, self.boatcarry)
      for adj_node in adj_nodes:
        inCL = False
        for closed_node in self.closed_list:
          if adj_node == closed_node:
            if (transfer_node.g + 1 < closed_node.g):
              closed_node.g = transfer_node.g + 1
              closed_node.predecessor = transfer_node
              self.parentRedirection(closed_node)
            inCL = True
            break
        if (inCL):
          continue
        inOL = False
        for open_node in self.open_list:
          if (adj_node == open_node):
            if (transfer_node.g + 1 < open_node.g):
              open_node.g = transfer_node.g + 1
              open_node.predecessor = transfer_node
            inOL = True
            break
        if (inOL):
          continue
        adj_node.g = transfer_node.g + 1
        adj_node.predecessor = transfer_node
        self.open_list.put((adj_node.h + adj_node.g, adj_node))

    print(siddu_steps)
    if transfer_node.missionaries == 0 and transfer_node.cannibals == 0 and transfer_node.boatpos == 'R':
      print("Path:")
      transfer_node.printPath()
  def parentRedirection(self, node):
    adj_nodes = node.getAdjacentNodes(self.maxm, self.maxc, self.boatcarry)
    for adj_node in adj_nodes:
      for closed_node in self.closed_list:
        if adj_node == closed_node:
          if node.g + 1 < closed_node.g:
            closed_node.g = node.g + 1
            closed_node.predecessor = node
            self.parentRedirection(closed_node)
          break

