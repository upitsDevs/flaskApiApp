#!/usr/bin/python
try:
    from flask import request
    from flask_api import FlaskAPI
    import RPi.GPIO as GPIO
    import Adafruit_DHT
    from datetime import datetime, date, time, tzinfo
    from flask_cors import CORS


    LEDS = {"blue": 10, "red": 8}
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LEDS["blue"], GPIO.OUT)
    GPIO.setup(LEDS["red"], GPIO.OUT)
    sensor=Adafruit_DHT.DHT11 
    dhtPort = 17
    
    app = FlaskAPI(__name__)
    CORS(app)

    @app.route('/', methods=["GET"])
    def api_root():
        return {
               "led_url": request.url + "led/(blue | red)/",
                 "led_url_POST": {"state": "(0 | 1)"}
                     }
    @app.route('/status', methods=["GET"])
    def api_status():
        return {
               'status':'connetced'
                     }
    @app.route('/temp', methods=["GET"])
    def api_temp():
        humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtPort)
        return {
               'temperature': '{0:0.1f}C'.format(temperature),
               'humidity': "{0:0.1f}".format(humidity),
               'status':'connetced',
               'last_update': datetime.now(),
        }
    @app.route('/led/<color>/', methods=["GET", "POST"])
    def api_leds_control(color):
        if request.method == "POST":
            if color in LEDS:
                GPIO.output(LEDS[color], int(request.data.get("state")))
        return {color: GPIO.input(LEDS[color])}
    
    
    if __name__ == "__main__":
        app.run(host='0.0.0.0')
except KeyboardInterrupt:
    print("W: interrupt received, stopping?")
finally:
    GPIO.cleanup()
