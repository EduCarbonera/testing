from flask import Blueprint, request, render_template, redirect, url_for

actuators_module = Blueprint("actuators", __name__, template_folder="templates")

devices = {"teste": "Servo Motor", "2":"4"}

@actuators_module.route("/actuators")
def actuators():
    global devices
    return render_template('actuators.html', actuators=devices)



@actuators_module.route('/register_actuator')
def register_actuator():
    return render_template("register_actuator.html")




@actuators_module.route('/add_actuator', methods=['GET','POST'])
def add_actuator():
    global devices
    if request.method == 'POST':
        actuator = request.form['actuator']
        value = request.form['value']
    else:
        actuator = request.args.get('actuator', None)
        value = request.args.get('value', None)
    devices[actuator] = value
    return render_template("actuators.html", actuators=devices)



@actuators_module.route('/list_actuators')
def list_actuators():
    global devices
    return render_template("actuators.html", actuators=devices)

@actuators_module.route('/remove_actuator')
def remove_actuator():
    return render_template("remove_actuator.html", actuators=devices)

@actuators_module.route('/del_actuator', methods=['GET','POST'])
def del_actuator():
    global devices
    if request.method == 'POST':
        actuator = request.form['actuator']
    else:
        actuator = request.args.get('actuator', None)
    devices.pop(actuator)
    return render_template("actuators.html", actuators=devices)
