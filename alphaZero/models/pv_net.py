import keras
from keras.engine.training import Model
from keras.layers import Input, Conv2D, Flatten, Dense
from keras.regularizers import l2
from keras.optimizers import Adam
from keras import backend as K

import numpy as np

import pickle


class PolicyValueNet:
    def __init__(self, row: int, col: int, actions: dict, model_file=None):
        """
        :param actions: all actions dictionary, key is action, value is index
        """
        self.row = row
        self.col = col
        self.actions = actions
        self.l2_const = 1e-4  # coef of l2 penalty
        self.policy_net, self.value_net, self.model = self.create_model()
        if model_file:
            net_params = pickle.load(open(model_file, 'rb'))
            self.model.set_weights(net_params)

    def create_model(self):
        in_x = conv_net = Input((4, self.row, self.col))

        conv_net = Conv2D(filters=32, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(conv_net)
        conv_net = Conv2D(filters=64, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(conv_net)
        conv_net = Conv2D(filters=128, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(conv_net)

        # policy net
        policy_net = Conv2D(filters=4, kernel_size=(1, 1), activation="relu", data_format="channels_first",
                            kernel_regularizer=l2(self.l2_const))(conv_net)
        policy_net = Flatten()(policy_net)
        policy_net = Dense(len(self.actions), activation="softmax",
                           kernel_regularizer=l2(self.l2_const))(policy_net)

        # value net
        value_net = Conv2D(filters=2, kernel_size=(1, 1), activation="relu", data_format="channels_first",
                           kernel_regularizer=l2(self.l2_const))(conv_net)
        value_net = Flatten()(value_net)
        value_net = Dense(64, kernel_regularizer=l2(self.l2_const))(value_net)
        value_net = Dense(1, activation="tanh", kernel_regularizer=l2(self.l2_const))(value_net)

        model = Model(in_x, [policy_net, value_net])

        return policy_net, value_net, model

    def _loss_train_op(self):
        """
        Three loss terms：
        loss = (z - v)^2 + pi^T * log(p) + c||theta||^2
        """

        # get the train op
        opt = Adam()
        losses = ['categorical_crossentropy', 'mean_squared_error']
        self.model.compile(optimizer=opt, loss=losses)

        def self_entropy(probs):
            return -np.mean(np.sum(probs * np.log(probs + 1e-10), axis=1))

        def train_step(state_input, mcts_probs, winner, learning_rate):
            state_input_union = np.array(state_input)
            mcts_probs_union = np.array(mcts_probs)
            winner_union = np.array(winner)
            loss = self.model.evaluate(state_input_union, [mcts_probs_union, winner_union], batch_size=len(state_input),
                                       verbose=0)
            action_probs, _ = self.model.predict_on_batch(state_input_union)
            entropy = self_entropy(action_probs)
            K.set_value(self.model.optimizer.lr, learning_rate)
            self.model.fit(state_input_union, [mcts_probs_union, winner_union], batch_size=len(state_input), verbose=0)
            return loss[0], entropy

        self.train_step = train_step

    def evaluate(self, reshaped_state, available_actions):
        policies, values = self.model.predict_on_batch(reshaped_state)
        policies = policies.flatten()
        action_probs = {available_actions[i]: policies[i] for i in range(len(available_actions))}
        return action_probs, values[0][0]

    def save_model(self, model_file):
        """ save model params to file """
        net_params = self.model.get_weights()
        pickle.dump(net_params, open(model_file, 'wb'), protocol=2)
