NYC Capital Projects (SANDBOX)
==============================

This project is an exploratory sandbox with which I seek to rebuild portions of an existing analysis of New York City-managed capital projects. The original analysis from which this repository borrows used different approaches to modeling and feature engineering to predict budget and schedule outcomes for NYC capital projects with budgets greater than $25 million, using a `data set hosted by NYC Open Data`_.

.. image:: https://github.com/sedelmeyer/caproj-sandbox/workflows/build/badge.svg?branch=master
    :target: https://github.com/sedelmeyer/caproj-sandbox/actions


.. Note::

   **This project is primarily being constructed for my own personal learning experience, where my current area of focus are approaches to generating tested and log-generating data pipelines. As such:**

   * Please disregard existing project releases, because they do not adhere to semantic versioning standards.

     * There is a chance that I may stabilize future releases, but that will be entirely dependent on how long I continue to work on this repository.

   * Please also disregard existing project documentation, which is currently not a focus of my current efforts.


.. contents:: Contents
  :local:
  :depth: 1
  :backlinks: none

Summary
-------

This original analysis from which this one borrows was initially completed as a final project for `CS109B: Advanced Topics In Data Science`_, a course offered by Harvard University's John A. Paulson School of Engineering and Applied Sciences (SEAS). The authors of that original project are:

- `An Hoang <https://github.com/hoangthienan95>`_
- `Mark McDonald <https://github.com/mcdomx>`_
- `Mike Sedelmeyer <https://github.com/sedelmeyer>`_

That original project can be found on GitHub at: https://github.com/mcdomx/cs109b_groupproject. The final report summarizing the methods and findings for that project can be found in the `Jupyter notebook-based report for that project <https://github.com/mcdomx/cs109b_groupproject/blob/master/notebooks/Module-E-final-report-Group71.ipynb>`_.

Research question
^^^^^^^^^^^^^^^^^

After initial exploration and cleansing of the available data, modeling efforts focus on the following research question:

- *Using very limited historical project data, can we predict how much the forecasted budget and duration of any given capital project run by the City of New York will deviate from its original budgeted estimates by the end of year-3 for the project?*


Analysis and findings
---------------------

The analysis and findings associated with this project can be found here:

https://sedelmeyer.github.io/nyc-capital-projects


Source code documentation
-------------------------

Documentation for the python modules built specifically for this analysis (i.e. modules located in the ``./src/`` directory of this project) can be found here:

https://sedelmeyer.github.io/nyc-capital-projects/modules.html


.. _data set hosted by NYC Open Data: https://www1.nyc.gov/site/capitalprojects/dashboard/category.page?category=All%20Capital%20Projects

.. _`CS109b: Advanced Topics In Data Science`: https://harvard-iacs.github.io/2020-CS109B/
