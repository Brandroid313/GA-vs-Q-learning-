import json
import random


class Bot(object):
    """
    The Bot class that applies the Qlearning logic to Flappy bird game
    After every iteration (iteration = 1 game that ends with the bird dying) updates Q values
    """

    def __init__(self):
        self.gameCNT = 0  # Game count of current run, incremented after every death
        self.discount = 1.0
        self.r = {0: 0, 1: -1000}  # Reward function
        self.lr = 0.7
        self.load_qvalues()
        self.last_state = "0_0_0_0" # initial position, MUST NOT be one of any other possible state
        self.initStateIfNull(self.last_state)
        self.last_action = 0
        self.moves = []

    def load_qvalues(self):
        """
        Load q values from a JSON file
        """
        self.qvalues = {}
        try:
            fil = open("data/qvalues.json", "r")
        except IOError:
            return
        self.qvalues = json.load(fil)
        fil.close()

    def showStep(self, num, state, action, new_state):
        print("{0:5d}: ({1:15s}:{2:6d}, {3:1d}): {4:6.0f} => ({5:15s}): {6:6.0f}, {7:6.0f}, {8:6d}"
            .format(num+1, state, self.qvalues[state][2], action, self.qvalues[state][action],
                    new_state, self.qvalues[new_state][0], self.qvalues[new_state][1], self.qvalues[new_state][2]))

    def showSteps(self, steps):
        start = 0 if len(steps) < 51 else len(steps) - 50
        for num, step in enumerate(steps[start:]):
            state, action, new_state = step
            self.showStep(num, state, action, new_state)

    def act(self, x, y, vel, pipe):
        """
        Chooses the best action with respect to the current state - Chooses 0 (don't flap) to tie-break
        """
        state = self.get_state(x, y, vel, pipe)

        self.moves.append(
            (self.last_state, self.last_action, state)
        )  # Add the experience to the history
 
        self.save_qvalues()

        action = 0 if self.qvalues[state][0] >= self.qvalues[state][1] else 1

        # if(action):
        #     print("Jumped by myself!")

        #print("Qvalues length: " + str(len(self.qvalues)))

        # if(len(self.qvalues) < 10000 and len(self.qvalues) % 50 == 0):
        #     action = 1
        rand = random.randrange(100)
        #print("Random:" + str(rand))
        # if(not action and rand >= 80 and self.gameCNT < 100):
        #      action = 1

        self.last_state = state  # Update the last_state with the current state
        self.last_action = action
        #print("%s -> %d" % (state, action))
        return action

    def initStateIfNull(self, state):
        if self.qvalues.get(state) == None:
             self.qvalues[state] = [0, 0, 0]  # [Q of no action, Q of flap action, Num of enter]
             num = len(self.qvalues.keys())
            #  if num > 20000 and num % 1000 == 0:
            #     print("======== Total state: {} ========".format(num))
            #  if num > 30000:
            #     print("======== New state: {0:14s}, Total: {1} ========".format(state, num))

    # terminate game and save q-values, the bird is still alive
    def terminate_game(self):
        history = list(reversed(self.moves))
        for exp in history:
            state, act, new_state = exp
            self.qvalues[state][act] = (1-self.lr) * self.qvalues[state][act] + \
                                   self.lr * ( self.r[0] + self.discount*max(self.qvalues[new_state][0:2]) )
        self.last_state = "0_0_0_0" # initial position, MUST NOT be one of any other possible state
        self.last_action = 0
        self.moves = []
        self.gameCNT += 1

    # save q-values during the game, the bird is still alive, just to reduce the memory consumption
    def save_qvalues(self):
        #print(len(self.moves))
        if len(self.moves) > 6_000_000:
            history = list(reversed(self.moves[:5_000_000]))
            for exp in history:
                state, act, new_state = exp
                self.qvalues[state][act] = (1-self.lr) * self.qvalues[state][act] + \
                                       self.lr * ( self.r[0] + self.discount*max(self.qvalues[new_state][0:2]) )
            self.moves = self.moves[5_000_000:]

    def update_scores(self, died, score=False, printLogs=False):
        """
        Update qvalues via iterating over experiences
        """
        history = list(reversed(self.moves))

        #print("in update scores, Self.moves, reversed:" + str(history))


        # Q-learning score updates
        # Flag if the bird died in the top pipe
        #high_death_flag = True if int(history[0][2].split("_")[1]) > 120 else False

        #t = 0
        # last_flap = True    # penalty for last flap action
        for exp in history:
            # t += 1
            state = exp[0]
            act = exp[1]
            new_state = exp[2]

            self.qvalues[state][2] += 1

            # Select reward
            # if t <= 2:
            #     cur_reward = self.r[1]
            #     if act: last_flap = False
            # elif (last_flap ) and act:
            #     cur_reward = self.r[1]
            #     #high_death_flag = False
            #     last_flap = False
            # else:
            #     cur_reward = self.r[0]

            # Select reward
            if died and act:
                cur_reward = self.r[1]
            elif died:
                cur_reward = self.r[1]
            elif score:
                cur_reward = self.r[0] + 1
            else:
                cur_reward = self.r[0]

            self.initStateIfNull(state)
            self.qvalues[state][act] = (1-self.lr) * self.qvalues[state][act] + \
                                       self.lr * ( cur_reward + self.discount*max(self.qvalues[new_state][0:2]) )


        printLogs = False
        if printLogs: self.showSteps(self.moves)
        if not score:
            self.gameCNT += 1  # increase game count
        self.moves = []  # clear history after updating strategies

    def get_state(self, x, y, vel, pipes):
        """
        format:
            x0_y0_v_y1

        (x, y): coordinates of player (top left point)
        x0: diff of x to next pipe x
        y0: diff of y to next pipe y
        v: current velocity
        """
       

        # If the bird is already past the pipe

        next_pipe = pipes[0]
        if (next_pipe.x) <= x - 50:
            next_pipe = pipes[1]
        

        #y1 should be the bottom of the bottom pipe
        # x location of pipes
        # y location of top pipe rim
        # y location of bottompipe rim

        x0 = x - next_pipe.x 
        y0 = y - next_pipe.bottom
        y1 = y - (abs(next_pipe.bottom - next_pipe.pipe_gap))

        
        state = str(int(x0)) + "_" + str(int(y0)) + "_" + str(int(vel)) + "_" + str(int(y1))
        self.initStateIfNull(state)
        #state = str(int(x0)) + "_" + str(int(y0)) + "_" + str(int(vel))
        
        return state


    def dump_qvalues(self, force=False):
        """
        Dump the qvalues to the JSON file
        """
        if force:
            print("******** Saving Q-table(%d keys) to local file... ********" % len(self.qvalues.keys()))
            fil = open("data/qvalues.json", "w")
            json.dump(self.qvalues, fil)
            fil.close()
            print("******** Q-table(%d keys) updated on local file ********" % len(self.qvalues.keys()))
