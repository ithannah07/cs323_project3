# cs323_project3
data privacy-project 3 by Hyeoseo Lee

How to reproduce my results:

This project runs using randomly generated input values between 0 and 100.
Because of this randomness, the exact numeric results or graph may not be identical to mine,
but you will obtain a very similar trend and outcome.

The values of n are fixed as [5, 10, 25, 50, 100].
When you run the code, it automatically performs five runs for each n,
computes the average runtime for each method (Non-private, Paillier, and Shamir),
and then generates a graph showing the runtime differences among the three methods.

To run:
python project3.py

The resulting graph ("average_runtime.png") will be saved automatically.


