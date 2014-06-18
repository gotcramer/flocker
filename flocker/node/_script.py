
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import StandardIOEndpoint
from twisted.protocols.basic import NetstringReceiver

from ._deploy import deploy

class Deployer(NetstringReceiver):
    def __init__(self):
        self.result = Deferred()

    def stringReceived(self, data):
        self.result.callback(data)


class DeployScript(object):
    def __init__(self, sys_module):
        self.sys_module = sys_module

    def main(self, reactor):
        protocol = Deployer()
        StandardIO(protocol=protocol, reactor=reactor)
        protocol.result.addCallback(safe_load)
        protocol.result.addCallback(deploy)
    
