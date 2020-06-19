import lang_types
separator = ':'

class State():
    
    def __init__(self):
        self.namespaces = {'root':{}
                          }
        
    def get_variable(self,name,space_path):
        path = self.get_variable_path(name,space_path)
        if path!= None:
            return self.namespaces[path][name]
        return lang_types.Null()
    
    def get_variable_path(self,name,space_path):
        for i in range(len(space_path),-1,-1):
            namespace = separator.join(space_path[0:i])
            if namespace in self.namespaces:
                if name in self.namespaces[namespace]:
                    return namespace
        return None
    
    def set_variable(self,name,space_path,variable):
        namespace = separator.join(space_path)
        if namespace in self.namespaces:
            self.namespaces[namespace][name] = variable
        
            
    def create_variable(self,name,space_path,variable):
        namespace = separator.join(space_path)
        self.namespaces[namespace][name] = variable
        
    def create_namespace(self,space_path):
        namespace = separator.join(space_path)
        self.namespaces[namespace] = {}
        
    def remove_namespace(self,space_path):
        namespace = separator.join(space_path)
        del self.namespaces[namespace]
        