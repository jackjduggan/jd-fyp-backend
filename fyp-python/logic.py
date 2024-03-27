from flask_app import unique_id, hostname, provider, operating_system, cpu_cores
"""
The purpose of this script is to direct the pipeline depending
upon the request details
"""

# brainstorm
# what are the things that make a big difference on the process?
# uid: no
# hostname: no
# provider: yes
# cpu:cores: kinda, depending on provider
#   could do a thing -> if gpc - cpucores=1 = e2.micro
#                       else if aws = t2.micro
# operating system: kinda - same thing with AMIs

