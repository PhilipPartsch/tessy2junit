###########
tessy2junit
###########

Implements a script to convert TESSY XML reports into JUnit XML format.

You can find the script under `scripts/tessy2junit.py <https://github.com/PhilipPartsch/tessy2junit/blob/main/scripts/tessy2junit.py>`__.

A script to anonymize Tessy reports is availalbe under `scripts/anonymize.py <https://github.com/PhilipPartsch/tessy2junit/blob/main/scripts/anonymize.py>`__.



A solution from Tessy is availabe here: https://www.razorcat.com/files/files/tessy/TESSY_5.1.x/TESSY_UserManual_51.pdf

In Chapter ``6.17.5 Execution and result evaluation`` you can find the description.

With command

.. code-block:: console

   tessycmd xslt [-xsl <XSL file>] [-o <output file>] <XML file>

and xlst file
``C:\Program Files\Razorcat\TESSY_5.x\bin\plugins\com.razorcat.tessy.reporting.templates\5.x\ci\TESSY_TestDetails_Report_JUnit.xsl``
you can transform your TESSY XML report into JUnit format.
