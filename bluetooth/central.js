var noble = require('noble');

var allowed_devices = require('./../bt_devices.json');

const LAMP_SERVICE = '0001a7d3d8a44fea81741736e808c066';

var LampiOnOffCharacteristic = null;
var onOffState;

// List of allowed devices
const devices = allowed_devices.devices;

noble.on('discover', function (peripheral) {
  if (devices.indexOf(peripheral.address.toUpperCase()) < 0) return;

  noble.stopScanning();

  peripheral.connect(function (err) {
    console.log('connected!');

    /*
    peripheral.discoverAllServicesAndCharacteristics(function (error, services, characteristics) {
         services.forEach(function (service) {
           console.log('found service:', service.uuid);
         });

         characteristics.forEach(function (characteristic) {
           console.log('found characteristic:', characteristic.uuid);
         });
    });
    */

    peripheral.discoverServices([LAMP_SERVICE], function (err, services) {
      console.log(services)

      services.forEach(function (service) {
        console.log('found service:', service.uuid);

        service.discoverCharacteristics([], function (err, characteristics) {
          characteristics.forEach(function (characteristic) {
            console.log('found characteristic:', characteristic.uuid);

            if (characteristic.uuid === '0004a7d3d8a44fea81741736e808c066') {
              LampiOnOffCharacteristic = characteristic;
              setInterval(togglePower, 500);
            }
          }); // characterisics
        }); // discover characteristics

      }); //services
    }); // discover services
  }); // connect
});

noble.on('stateChange', function (state) {
  if (state != "poweredOn") {
    noble.stopScanning();
    return;
  }

  console.log("Starting scan...");
  noble.startScanning([], true);
});

noble.on('scanStart', function () {
  console.log("Scanning started.");
});

noble.on('scanStop', function () {
  console.log("Scanning stopped.");
});

function togglePower() {
  LampiOnOffCharacteristic.read(function (err, data) {
    if (!err) {
      var power = new Buffer(1);
      if (data[0] === 1) {
        power.writeUInt8(0x0, 0);
      } else {
        power.writeUInt8(0x1, 0);
      }
      LampiOnOffCharacteristic.write(power, false, function (err) {
        if (!err) {
          console.log("success");
        } else {
          console.log("error");
        }
      });
    } else {
      console.log("error");
    }
  });
}

