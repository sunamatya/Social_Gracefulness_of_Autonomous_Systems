import numpy as np
# TODO pytorch version
import torch as t


class DecisionModel:
    def __init__(self, model, sim):
        self.sim = sim
        if model == 'constant_speed':
            self.plan = self.constant_speed
        elif model == 'complete_information':
            self.plan = self.complete_information
        elif model == 'reactive_point':
            self.plan = self.reactive_point
        elif model == 'reactive_uncertainty':
            self.plan = self.reactive_uncertainty
        else:
            # placeholder for future development
            pass

    @staticmethod
    def constant_speed():
        return {'action': 0}  # just keep the speed

    def complete_information(self, *args):
        # TODO: generalize for n agents

        # find nash equilibrial policies when intents (t1, t2) are known
        states, actions, intents = args  # state of agent 1, 2; latest actions 1, 2; intent of agent 1, 2

        loss = [self.create_long_term_loss(states, actions, intents[i]) for i in range(len(intents))]
        # iterate to find nash equilibrium
        # TODO: check convergence
        learning_rate = self.sim.par.learning_rate_planning
        optimizers = [t.optim.Adam(actions[i], lr=learning_rate) for i in range(len(intents))]
        for j in range(self.sim.par.max_iter_planning):
            for i in range(len(intents)):
                optimizers[i].zero_grad()
                loss[i].backward()
                optimizers[i].step()

    def baseline(self):
        # randomly pick one of the nash equilibrial policy
        pass

    def reactive_point(self):
        # implement reactive planning based on point estimates of future trajectories
        pass

    def reactive_uncertainty(self):
        # implement reactive planning based on inference of future trajectories
        pass

    # create long term loss as a pytorch object
    def create_long_term_loss(self, states, action1, action2, intent):
        # define instantaneous loss
        def loss(x, u1, u2, i):

            pass

        steps = self.sim.duration - self.sim.env.frame  # time left
        l = t.tensor(0)
        for i in range(steps):
            # compute instantaneous loss
            l = l + loss(states, action1[i], action2[i], intent)

            # update state
            states = self.sim.update(states, [action1[i], action2[i]])

        return l
