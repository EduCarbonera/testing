from flask import Blueprint, request, render_template, redirect, url_for

sensors_module = Blueprint("sensors", __name__, template_folder="templates")

devices = {
"Teste":1,
"Sensor de Umidade":20
}

@sensors_module.route('/sensors')
def sensors():
    global devices
    return render_template('sensors.html', sensors=devices)

@sensors_module.route('/register_sensor')
def register_sensor():
    return render_template("register_sensor.html")

@sensors_module.route('/add_sensor', methods=['GET','POST'])
def add_sensor():
    global devices
    if request.method == 'POST':
        sensor = request.form['sensor']
        value = request.form['value']
    else:
        sensor = request.args.get('sensor', None)
        value = request.args.get('value', None)
    devices[sensor] = value
    return render_template("sensors.html", sensors=devices)

@sensors_module.route('/list_sensors')
def list_sensors():
    global devices
    return render_template("sensors.html", sensors=devices)

@sensors_module.route('/remove_sensor')
def remove_sensor():
    return render_template("remove_sensor.html", sensors=devices)

@sensors_module.route('/del_sensor', methods=['GET','POST'])
def del_sensor():
    global devices
    if request.method == 'POST':
        sensor = request.form['sensor']
    else:
        sensor = request.args.get('sensor', None)
    devices.pop(sensor)
    return render_template("sensors.html", sensors=devices)