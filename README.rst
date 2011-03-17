=================
ClearQuest to RST
=================

A docutils for converting ClearQuest requests to RST tables.

Syntax
------

The syntax of the directive is as follows: ::

    .. clearquest:: <full name/of the clearquest query>
        :username: <your username>
        :password: <your password>
        :db_name: <the name of the db>
        :db_set: <the name of the db set>
        :params: <parameters to pass to the query> (optional)

The parameters to pass to the query must respect the following syntax: ::

    <param1_name>=<param1_value>,<param2_name>=<param2_value>, ....

You can provide them in any order as long as you don't forget one. 
The query call will fail if you do.

Required python libraries
-------------------------

* docutils: http://docutils.sourceforge.net/
* PyWin32: http://sourceforge.net/projects/pywin32/
* docutils-extensions: https://github.com/robin-jarry/docutils-extensions (optional)
