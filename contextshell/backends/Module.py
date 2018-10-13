
class Module:
    def register_actions(self):
        raise NotImplementedError()
    def unregister_actions(self):
        raise NotImplementedError()

    #Implement me please and make FilesystemModule loadable