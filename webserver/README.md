## Testing
To test an app over an unsecured connection, execute `bokeh serve <filename> --port <portnum>`.

## Deployment
To securely deploy an app,
[configure an nginx reverse proxy with SSL](https://bokeh.pydata.org/en/latest/docs/user_guide/server.html#reverse-proxying-with-nginx-and-ssl).

Then execute
`bokeh serve <filename/directory> --use-xheaders --allow-websocket-origin=<domain> --port <portnum>`.

Example:
`bokeh serve test_app.py --use-xheaders --allow-websocket-origin=pdeng.student.rit.edu --port 5006`
`bokeh serve app --use-xheaders --allow-websocket-origin=pdeng.student.rit.edu --port 5006`


## Dependencies
pip3 install mysql-connector-python
pip3 install bokeh
pip3 install pandas
pip3 install joblib
