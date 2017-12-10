# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        currFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        currGhostStates = currentGameState.getGhostStates()

        "*** YOUR CODE HERE ***"
        score=0
        food=currFood.asList()
        dists=[]
        closest_food=()
        for i in range(len(food)):
            dists.append(util.manhattanDistance(currPos,food[i]))
            if(util.manhattanDistance(currPos,food[i]))==min(dists):
                closest_food=food[i]
        for g in currGhostStates:
            if newPos == g.getPosition():
                score += -5
        for g in newGhostStates:
            if newPos == g.getPosition():
                score += -5
        for g in newGhostStates:
            if currPos == g.getPosition() and action == 'Stop':
                score += -5

        if action == 'North' and closest_food[1] > currPos[1]:
            score += 1
        if action == 'South' and closest_food[1] < currPos[1]:
            score += 1
        if action == 'West' and closest_food[0] < currPos[0]:
            score += 1
        if action == 'East' and closest_food[0] > currPos[0]:
            score += 1
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        value_per_move = []
        moves = gameState.getLegalActions(0)
        for i in range(len(moves)):
            value_per_move.append(self.minimax_value(gameState.generateSuccessor(0, moves[i]), 0, 1))
        for i in range(len(value_per_move)):
            if value_per_move[i] == max(value_per_move):
                return moves[i]

    def minimax_value(self, gameState, depth, agent):
        if agent == gameState.getNumAgents():
            agent = 0
            depth += 1
        if depth == self.depth or gameState.isWin() or gameState.isLose():
               return self.evaluationFunction(gameState)
        if agent == 0:
            minimax = float("-inf")
            for move in gameState.getLegalActions(agent):
                minimax = max(minimax, self.minimax_value(gameState.generateSuccessor(agent, move), depth, agent+1))
        else:
            minimax = float("inf")
            for move in gameState.getLegalActions(agent):
                minimax = min(minimax, self.minimax_value(gameState.generateSuccessor(agent, move), depth, agent+1))
        return minimax

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value_per_move = []
        moves = gameState.getLegalActions(0)
        a = float("-inf")
        b = float("inf")
        for i in range(len(moves)):
            value_per_move.append(self.minimax_value(gameState.generateSuccessor(0, moves[i]), 0, 1, a, b))
            a = max(a, value_per_move[i])
        for i in range(len(value_per_move)):
            if value_per_move[i] == max(value_per_move):
                return moves[i]

    def minimax_value(self, gameState, depth, agent, a, b):
        if agent == gameState.getNumAgents():
            agent = 0
            depth += 1
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent == 0:
            v = float("-inf")
            for move in gameState.getLegalActions(agent):
                v = max(v, self.minimax_value(gameState.generateSuccessor(agent, move), depth, agent + 1, a, b))
                if v > b:
                    return v
                a = max(a,v)
        else:
            v = float("inf")
            for move in gameState.getLegalActions(agent):
                v = min(v, self.minimax_value(gameState.generateSuccessor(agent, move), depth, agent + 1, a, b))
                if v < a:
                    return v
                b = min(b,v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        value_per_move = []
        moves = gameState.getLegalActions(0)
        for i in range(len(moves)):
            value_per_move.append(self.expectiminimax_value(gameState.generateSuccessor(0, moves[i]), 0, 1))
        for i in range(len(value_per_move)):
            if value_per_move[i] == max(value_per_move):
                return moves[i]

    def expectiminimax_value(self, gameState, depth, agent):
        if agent == gameState.getNumAgents():
            agent = 0
            depth += 1
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent == 0:
            expectiminimax = float("-inf")
            for move in gameState.getLegalActions(agent):
                expectiminimax = max(expectiminimax, self.expectiminimax_value(gameState.generateSuccessor(agent, move), depth, agent + 1))
        else:
            expectiminimax = 0
            for move in gameState.getLegalActions(agent):
                expectiminimax += self.expectiminimax_value(gameState.generateSuccessor(agent, move), depth, agent + 1) / len(gameState.getLegalActions(agent))
        return expectiminimax

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    pacman_pos = currentGameState.getPacmanPosition()
    capsule_pos = currentGameState.getCapsules()
    food_pos = currentGameState.getFood().asList()
    ghost_states = currentGameState.getGhostStates()
    food_dist = []
    ghost_dist = []
    capsule_dist = []
    if currentGameState.isWin() or currentGameState.isLose():
        score *= 10
        return score
    for i in food_pos:
        food_dist.append(util.manhattanDistance(pacman_pos, i))
    for i in ghost_states:
        ghost_dist.append(util.manhattanDistance(pacman_pos, i.getPosition()))
    for i in capsule_pos:
        capsule_dist.append(util.manhattanDistance(pacman_pos, i))
    for g in ghost_states:
        if pacman_pos == g.getPosition():
            score /= 2
    minf = min(food_dist)
    ming = min(ghost_dist)
    score += ming / minf
    """the smaller the distance to the closest food, the bigger the value"""
    """the bigger the distance to the closest ghost, the bigger the value"""
    if len(capsule_dist) != 0:
        """if a capsule is closer than a simple dot"""
        if min(capsule_dist) < minf:
            score += 10
    dif = ming - minf
    """the bigger the difference between closest ghost and closest food the faster the value scales"""
    for i in range(1, 10, 1):
        if dif >= i:
            score += i
    return score
# Abbreviation
better = betterEvaluationFunction

