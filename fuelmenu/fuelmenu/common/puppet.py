import subprocess
import sys
import logging

#Python 2.6 hack to add check_output command

<<<<<<< HEAD
if "check_output" not in dir(subprocess):  # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, \
itwill be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs,
                                   **kwargs)
=======
if "check_output" not in dir( subprocess ): # duck punch it in!
    def f(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
>>>>>>> 265265e6e18510422b50eba78bac1483d41e5052
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise Exception(retcode, cmd)
        return output
    subprocess.check_output = f

<<<<<<< HEAD

def puppetApply(classname, name=None, params=None):
    #name should be a string
    #params should be a dict
    '''Runs puppet apply -e "classname {'name': params}" '''
    log = logging
    log.basicConfig(filename='./fuelmenu.log', level=logging.DEBUG)
    log.info("Puppet start")

    command = ["puppet", "apply", "-d", "-v", "--logdest", "/tmp/puppet.log"]
    input = [classname, "{", '"%s":' % name]
    #Build params
    for key, value in params.items():
        if type(value) == bool:
            input.extend([key, "=>", '%s,' % str(value).lower()])
        else:
            input.extend([key, "=>", '"%s",' % value])
    input.append('}')

    log.debug(' '.join(command))
    log.debug(' '.join(input))
    output = ""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        output, errout = process.communicate(input=' '.join(input))[0]
    except Exception, e:
        import traceback
        log.error(traceback.print_exc())
        log.error(e)
        log.debug(output)
        log.debug(e)
        if "err:" in output:
            log.error(e)
            return False
        else:
            log.debug(output)
            return True
=======
def puppetApply(classname, name=None, params=None):
  '''Runs puppet apply -e "classname {'name': params}" '''
  log = logging
  log.basicConfig(filename='./fuelmenu.log',level=logging.DEBUG)
  log.info("Puppet start")

#name should be a string
#params should be a dict
#  command=["puppet","apply","-d","-v","--logdest","/tmp/puppet.log", "-e",'\'',classname,"{",'"%s":' % name]
#  #Build params
#  for key,value in params.items():
#     command.extend([key,"=>",'"%s",' % value])
#  command.append('{\'')
  command=["puppet","apply","-d","-v","--logdest","/tmp/puppet.log",]
  input=[classname,"{",'"%s":' % name]
  #Build params
  for key,value in params.items():
     input.extend([key,"=>",'"%s",' % value])
  input.append('}')
  
  log.debug(' '.join(command))
  log.debug(' '.join(input))
  output=""
  try:
    #output = subprocess.check_output(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
              stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errout = process.communicate(input=' '.join(input))[0]
    #output = subprocess.check_output(command)
  except Exception, e:
    import traceback
    log.error(traceback.print_exc())
    log.error(e)
    log.debug(output)
    log.debug(e)
    if "err:" in output:
      log.error(e)
    return False
  else:
    log.debug(output)
    return True
>>>>>>> 265265e6e18510422b50eba78bac1483d41e5052
