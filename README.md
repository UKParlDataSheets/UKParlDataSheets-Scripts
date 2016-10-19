# UKParlDataSheets - Scripts

The UKParlDataSheets website is at http://ukparldatasheets.jmbtechnology.co.uk/

These are the scripts that build and upload the data for that site.

## Setting up

This is written and tested on Python 2.7.

Needed libraries:

  *  boto3

Copy "config.py.dist" to "config.py" and edit.

The AWS user should have the putObject permission on the bucket.

## Running Project

To run unit tests:

    python tests.py

To build docs:

    pydoc -w funcs tests

To run scripts to create data but not upload (useful for local testing):

    python go.py

To run scripts to create data and upload:

    python goAndUpload.py

## In Production

The scripts are designed to be run in AWS Lambda.

Make a zip file of all *.py files and upload.

Configure Runtime: Python 2.7, Handler: lambda_function.lambda_handler

Set up a trigger to run the task on a regular basis.
