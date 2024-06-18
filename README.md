# eve_to_securecrt

Simple script used to convert an eve-ng lab instance to SecureCRT templates. EVE-NG changes the telnet port per login, making keeping up with sessions difficult.

## Tested on
- Python 3.12
- SecureCRT 8.5.4
- EVE-NG 5.0.1-129

## Setup
1. Clone the repo
`git clone https://github.com/jamesduv9/eve_to_securecrt.git`
2. Change to the directory
`cd eve_to_securecrt`
3. Install python libraries
`pip install -r requirements.txt`

## Run the script
eve_to_securecrt is a click cli tool, the create-template command has the following options. Note that eve-ip, eve-username, eve-password, and lab-name are required. output-directory is dynamically set to your securecrt sessions folder (if on windows), but you can change this to whatever you'd like

```bash
PS> python .\eve_to_securecrt.py create-templates --help
Usage: eve_to_securecrt.py create-templates [OPTIONS]

  Makes an api call to eve-ng getting all nodes in a lab

  Uses jinja to template out the device info into securecrt session templates

Options:
  --output-directory TEXT  Where to save the templated sessions  [default: C:\
                           Users\james\AppData\Roaming\VanDyke\Config\Sessions
                           ]
  --eve-ip TEXT            IP for your eve-ng instance- Ex. 192.168.1.241
                           [required]
  --eve-username TEXT      Username for your eve-ng instance- Ex. admin
                           [required]
  --eve-password TEXT      Password for your eve-ng instance- Ex. eve
                           [required]
  --lab-name TEXT          Lab name that you want sessions for- Ex. mylab
                           [required]
  --help                   Show this message and exit.
```

Run the script with required params
```bash
python eve_to_securecrt.py create_templates --eve-ip 192.168.1.120 --eve-username admin --eve-password eve --lab-name mylab123
```

## Template
The template file `securecrt_template.j2` can be modified to meet your exact requirement, like color syntax, etc.