===========
 Overview
===========

The problem
^^^^^^^^^^^
A lot of big companies have large websites that are constantly changing and are
dynamic. This is really nice in order to keep you brand/site up to date with new trends but it also
has a bad side effect. Old web pages get deleted and people opening them are getting 404
errors. Usually companies are familiar with that and they even know which old url should
redirect to which new one but unfortunately there isn't an easy way to do that in kubernetes at
the moment.

The solution
^^^^^^^^^^^^
The **Redirectory for Kubernetes** project aims to solve this problem once and for all of the
companies. It aims to provide a set of features which makes it easy for people of Kumina or
customers of Kumina to manage their redirects on their Kubernetes clusters. The project will live
on the ingress level in a cluster and will intercept all requests that the ingress is not able to
serve and otherwise would send out a 404. Redirectory will catch those errors and try to find the
best new url to redirect to in order for the customer to have a seamless experience even though
they might be using old and inactive urls.

