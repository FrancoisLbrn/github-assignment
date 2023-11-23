"""Assignment - making a sklearn estimator.

The goal of this assignment is to implement by yourself a scikit-learn
estimator for the OneNearestNeighbor and check that it is working properly.

The nearest neighbor classifier predicts for a point X_i the target y_k of
the training sample X_k which is the closest to X_i. We measure proximity with
the Euclidean distance. The model will be evaluated with the accuracy (average
number of samples corectly classified). You need to implement the `fit`,
`predict` and `score` methods for this class. The code you write should pass
the test we implemented. You can run the tests by calling at the root of the
repo `pytest test_sklearn_questions.py`.

We also ask to respect the pep8 convention: https://pep8.org. This will be
enforced with `flake8`. You can check that there is no flake8 errors by
calling `flake8` at the root of the repo.

Finally, you need to write docstring similar to the one in `numpy_questions`
for the methods you code and for the class. The docstring will be checked using
`pydocstyle` that you can also call at the root of the repo.
"""
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.utils.validation import check_X_y
from sklearn.utils.validation import check_array
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.multiclass import check_classification_targets
from sklearn.metrics import accuracy_score


class OneNearestNeighbor(BaseEstimator, ClassifierMixin):
    """OneNearestNeighbor classifier.

    Parameters
    ----------

    Attributes
    ----------
    classes_ : array, shape (n_classes,)
        The classes seen during fit.
    """

    def __init__(self):
        pass

    def fit(self, X, y):
        """Fit the OneNearestNeighbor classifier.

        Parameters
        ----------
        X : array or pd.DataFrame, shape (n_samples, n_features)
            Training data, where n_samples is the number of samples and
            n_features is the number of features.
        y : array or pd.Series, shape (n_samples,)
            Target values.

        Returns
        -------
        self : object
            Returns self.
        """
        X, y = check_X_y(X, y)
        check_classification_targets(y)
        self.classes_ = np.unique(y)
        self.n_features_in_ = X.shape[1]
        self.X_train_ = X
        self.y_train_ = y
        return self

    def predict(self, X):
        """Predict the target labels for the input data.

        Parameters
        ----------
        X : array or pd.DataFrame, shape (n_samples, n_features)
            Input data.

        Returns
        -------
        y_pred : array, shape (n_samples,)
            Predicted target labels.
        """
        check_is_fitted(self)
        X = check_array(X)

        # From LAB 2 KNN ML compute_distances_two_loops
        shape_train = np.shape(self.X_train_)[0]
        shape_test = np.shape(X)[0]
        dists = np.zeros((shape_test, shape_train))
        for i in range(shape_test):
            for j in range(shape_train):
                dists[i, j] = np.sqrt(
                    np.sum(np.square(X[i, :] - self.X_train_[j, :]))
                    )
        closest_idx = np.argmin(dists, axis=1)

        y_pred = self.y_train_[closest_idx]
        return y_pred

    def score(self, X, y):
        """Return the mean accuracy on the given test data and labels.

        Parameters
        ----------
        X : array or pd.DataFrame, shape (n_samples, n_features)
            Test samples.
        y : array or pd.Series, shape (n_samples,)
            True labels for X.

        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) with respect to y.
        """
        X, y = check_X_y(X, y)
        y_pred = self.predict(X)
        return accuracy_score(y, y_pred)
