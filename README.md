# lothian-bus-homeassistant
home assistant sensor for lothian buses

i recommend you don't use this yet -- it's working (just)

<p align="center"><img src="https://blog.codinghorror.com/content/images/uploads/2007/03/6a0120a85dcdae970b0128776ff992970c-pi.png"/></p>

## configuration
```
  - platform: lothian_bus
    stop_code: 36237859
    service_number: 67
    name: "Next 67 from Liberton Park"
```

you can find your stop code here; http://www.mybustracker.co.uk/
e.g. ![image](https://i.maccydee.com/u/22.01.43-13.12.18-44464.png)
