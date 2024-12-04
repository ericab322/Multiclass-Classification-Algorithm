import numpy as np

class BinaryLogisticRegression:
    def __init__(self, n_features, batch_size, epochs):
        """Initialize the binary logistic regression model.
        @param n_features: Number of features in the dataset, an integer.
        @param batch_size: Batch size for training, an integer.
        @param conv_threshold: Convergence threshold for training, a float.
        @return: None
        """
        self.n_features = n_features
        self.weights = np.zeros(n_features + 1)  # extra element for bias
        self.alpha = 0.03
        self.batch_size = batch_size
        self.epochs = epochs

    def sigmoid(self, z):
        '''
        Perform sigmoid operation
        @params:
            z: the input to which sigmoid will be applied
        @return:
            an array with sigmoid applied elementwise.
        '''
        return 1 / (1 + np.exp(-z))

    def train(self, X, Y):
        '''
        Trains the model using stochastic gradient descent
        @params:
            X: a 2D Numpy array where each row contains an example, padded by 1 column for the bias
            Y: a 1D Numpy array containing the corresponding labels for each example
        @return:
            num_epochs: integer representing the number of epochs taken to reach convergence
        '''
        # intializing values
        converge = False
        epochs = 0
        n_examples = X.shape[0]

        for epoch in self.epochs:
            # update # of epochs
            # acquire indices for shuffling of X and Y
            indices = np.arange(n_examples)
            np.random.shuffle(indices)
            X = X[indices]
            Y = Y[indices]
            # calc last epoch loss
            last_epoch_loss = self.loss(X, Y)
            # for the # of batches
            for i in range(0, n_examples, self.batch_size):
                X_batch = X[i:i + self.batch_size]
                Y_batch = Y[i:i + self.batch_size]
                # reinitialize gradient to be 0s
                grad = np.zeros(self.weights.shape)
                # for each pair in the batch
                for x, y in zip(X_batch, Y_batch):
                    prediction = self.sigmoid(np.dot(self.weights, x))
                    # gradient calculation
                    error = prediction - y
                    grad += error * x
                # update weights
                self.weights -= ((self.alpha * grad)/ self.batch_size)
            epoch_loss = self.loss(X, Y)

    def loss(self, X, Y):
        '''
        Returns the total log loss on some dataset (X, Y), divided by the number of examples.
        @params:
            X: 2D Numpy array where each row contains an example, padded by 1 column for the bias
            Y: 1D Numpy array containing the corresponding labels for each example
        @return:
            A float number which is the average loss of the model on the dataset
        '''
        n_examples = X.shape[0]
        total_loss = 0
        
        for i in range(n_examples):
            # linear output (dot product)
            linear_output = np.dot(self.weights, X[i])
            # calc logistic loss for each sample
            y = 1 if Y[i] == 1 else -1
            logistic_loss = np.log(1 + np.exp(-y * linear_output))
            total_loss += logistic_loss
    
        return total_loss / n_examples
    
    def predict(self, X):
        '''
        Compute predictions based on the learned weigths and examples X
        @params:
            X: a 2D Numpy array where each row contains an example, padded by 1 column for the bias
        @return:
            A 1D Numpy array with one element for each row in X containing the predicted class.
        '''
        # multiply X by weights of model
        predictions = self.sigmoid(X @ self.weights.T)
        return np.where(predictions >= 0.5, 1, 0)

    def accuracy(self, X, Y):
        '''
        Outputs the accuracy of the trained model on a given testing dataset X and labels Y.
        @params:
            X: a 2D Numpy array where each row contains an example, padded by 1 column for the bias
            Y: a 1D Numpy array containing the corresponding labels for each example
        @return:
            a float number indicating accuracy (between 0 and 1)
        '''
        predictions = self.predict(X)
        accuracy = np.mean(predictions == Y)
        return accuracy